# ~/projects/django-web-app/merchex/listings/views.py

from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import UploadFilesForm
from .models import DemandesTraiter, Quota
from django.core.files.storage import default_storage
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from io import BytesIO
import pandas as pd
from datetime import datetime
from collections import defaultdict

from dateutil.relativedelta import relativedelta

# Sample view for hello.html
def hello(request):
    bands = Band.objects.all()
    return render(request, 'listings/hello.html', {'bands': bands})

# View for displaying tables.html
def tables(request):
    # Your logic for this view
    return render(request, 'listings/tables.html')

def demandes(request):
    return render(request, 'listings/demandes.html')
    
def quota(request):
    quotas = Quota.objects.all()
    return render(request, 'listings/quota.html',{'quotas': quotas})

def agents(request):
    return render(request, 'listings/agents.html')

def historique(request):
    historiques=Historique.objects.all()
    return render(request, 'listings/historique.html',{'historiques': historiques})



# View for about page
def about(request):
    return HttpResponse('<h1>À propos</h1> <p>Nous adorons merch !</p>')

# View for uploading files
# View for uploading files
def upload_files(request):
    if request.method == 'POST':
        form = UploadFilesForm(request.POST, request.FILES)
        if form.is_valid():
            # Extract uploaded files
            agents_file = request.FILES.get('agents_file')
            historique_file = request.FILES.get('historique_file')
            demandes_file = request.FILES.get('demandes_file')
            
            # Extract date fields
            date_debut_sejour = request.POST.get('date_debut_sejour')
            date_fin_sejour = request.POST.get('date_fin_sejour')

            try:
                # Save files temporarily
                agents_path = default_storage.save('agents_file.xlsx', agents_file)
                historique_path = default_storage.save('historique_file.xlsx', historique_file)
                demandes_path = default_storage.save('demandes_file.xlsx', demandes_file)

                # Process the files
                process_files(agents_path, historique_path, demandes_path, date_debut_sejour, date_fin_sejour)

                # Redirect to the list_generated view
                return redirect('list_generated')

            except Exception as e:
                # Handle any exceptions that occur during file processing
                return HttpResponse(f"An error occurred: {e}")

    return render(request, 'listings/tables.html')


# View for listing generated data


def list_generated(request):
    # Fetch distinct combinations of 'ville' and 'type_de_vue'
    data = DemandesTraiter.objects.values('ville', 'type_de_vue').distinct()
    
    # Group data by 'ville' and store unique 'type_de_vue' values
    grouped_data = defaultdict(set)
    for item in data:
        grouped_data[item['ville']].add(item['type_de_vue'])
    
    # Convert set to list for rendering
    context = {
        'data': {ville: list(types) for ville, types in grouped_data.items()}
    }
    
    return render(request, 'listings/tables.html', context)


# View for downloading PDF
def download_pdf(request, ville, type_de_vue):
    # Retrieve data from the database
    data = get_data_from_database(ville, type_de_vue)
    df = pd.DataFrame(data)
    
    # Print column names to debug
    print("DataFrame columns:", df.columns.tolist())
    
    # Sort the DataFrame based on 'P' in descending order
    sorted_table = df.sort_values(by=['P'], ascending=[False]).reset_index(drop=True)
    
    # Define columns of interest based on the model
    columns_of_interest = ['numero_demande', 'ville', 'nom_agent', 'prenom_agent', 'matricule',
                           'date_debut_sejour', 'date_fin_sejour', 'type_de_vue', 'P']
    columns_of_interest_print = ['numero_demande', 'nom_agent', 'prenom_agent', 'matricule',
                                 'date_debut_sejour', 'date_fin_sejour','A','S','D', 'P']

    # Check if all columns exist in the DataFrame
    missing_cols = [col for col in columns_of_interest if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing columns: {missing_cols}")

    # Prepare the selected data
    selected_data = sorted_table[columns_of_interest_print].copy()
    selected_data['date_debut_sejour'] = pd.to_datetime(selected_data['date_debut_sejour']).dt.strftime('%Y-%m-%d')
    selected_data['date_fin_sejour'] = pd.to_datetime(selected_data['date_fin_sejour']).dt.strftime('%Y-%m-%d')

    # Get the quota value
    quota_value = get_quota_value(ville, type_de_vue)

    # Separate data into principal and waiting lists based on quota
    if (quota_value or 0) >= len(selected_data):
        principal_data = selected_data
        waiting_data = pd.DataFrame(columns=columns_of_interest_print)
    else:
        principal_data = selected_data.head(quota_value)
        waiting_data = selected_data.tail(len(selected_data) - quota_value)

    # Convert DataFrames to lists for PDF generation
    principal_data_list = [principal_data.columns.tolist()] + principal_data.values.tolist()
    waiting_data_list = [waiting_data.columns.tolist()] + waiting_data.values.tolist()

    # Define titles for the PDF
    title_text = f"Liste principale pour {ville} ({type_de_vue})"
    title_text_wait = f"Liste d'attente pour {ville} ({type_de_vue})"

    # Create the PDF
    pdf_data = create_pdf(principal_data_list, waiting_data_list, calculate_column_widths(selected_data), title_text, title_text_wait)
    
    # Return the PDF response
    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{ville}_{type_de_vue}.pdf"'
    
    return response


# Helper function to retrieve data from database
def get_data_from_database(ville, type_de_vue):
    return DemandesTraiter.objects.filter(ville=ville, type_de_vue=type_de_vue).values()


# Helper function to retrieve quota value
def get_quota_value(ville, type_de_vue):
    try:
        quota = Quota.objects.get(ville=ville, type_de_vue=type_de_vue)
        return quota.quota_value
    except Quota.DoesNotExist:
        return 0





# Helper function to calculate column widths for the table
def calculate_column_widths(data):
    col_widths = []
    for col in data.columns:
        if col != 'Type de vue':  # Exclude 'Type de vue' column
            max_len = max(data[col].astype(str).map(len).max(), len(col))  # Include header length
            col_widths.append(max_len * 8)  # Multiply by a factor to adjust width
    return col_widths



# Function to process uploaded files
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

def process_files(agents_path, historique_path, demandes_path, date_debut_sejour, date_fin_sejour):
    # Load data from Excel files
    historique_df = pd.read_excel(historique_path)
    agents_df = pd.read_excel(agents_path)
    demandes_df = pd.read_excel(demandes_path)
    
    # Filter rows based on date_debut_sejour and date_fin_sejour
    demandes_df = demandes_df[
        (demandes_df['Date debut sejour'] == date_debut_sejour) &
        (demandes_df['Date fin sejour'] == date_fin_sejour)
    ]
    # Create a new DataFrame 'demandes_traiter' that contains the exact content of the 'demandes' file
    demandes_traiter_df = demandes_df.copy()
  

    # ## Step 4: Filter Rows

    # Keep only rows where 'Site' is 'khouribga'
    demandes_traiter_df = demandes_traiter_df[demandes_traiter_df['Site'] == 'Khouribga']
   
    # Keep only rows where 'Nature Periode' is 'Bloquée'
    demandes_traiter_df = demandes_traiter_df[demandes_traiter_df['Nature Periode'] == 'Bloquée']
   

    # Keep only rows where 'Statut' is 'En attente de traitement'
    demandes_traiter_df = demandes_traiter_df[demandes_traiter_df['Statut'] == 'En attente de traitement']
   

    # ## Step 5: Add retraite Column and Calculate Its Values

    from datetime import datetime

    # Merge demandes_traiter_df with agents_df to get 'date_embauche', 'sit_fam', and 'NOMBRE_ENF'
    demandes_traiter_df = demandes_traiter_df.merge(agents_df[['matricule', 'date_embauche', 'sit_fam', 'NOMBRE_ENF','date_debut_retraite']], left_on='Matricule', right_on='matricule', how='left')
   


    # Convert 'Date_embauche' to datetime
    demandes_traiter_df['date_embauche'] = pd.to_datetime(demandes_traiter_df['date_embauche'], format='%d/%m/%Y')
    demandes_traiter_df['Date debut sejour'] = pd.to_datetime(demandes_traiter_df['Date debut sejour'], format='%d/%m/%Y')
    # Convert 'date_debut_retraite' to datetime if it's not already
    demandes_traiter_df['date_debut_retraite'] = pd.to_datetime(demandes_traiter_df['date_debut_retraite'],format='%d/%m/%Y')
    #filtrage expired date_debut_retraite:
    demandes_traiter_df= demandes_traiter_df[demandes_traiter_df['date_debut_retraite'] > demandes_traiter_df['Date debut sejour']]
   


    # ## Calculate A 

    from datetime import datetime
    from dateutil.relativedelta import relativedelta
    # Calculate 'A' as the difference between current date and 'Date_embauche' in months
    demandes_traiter_df['A'] = demandes_traiter_df['date_embauche'].apply(lambda x: relativedelta(datetime.now(), x).years * 12 + relativedelta(datetime.now(), x).months)


    # ## Calculate S 

    # Function to calculate 'S'
    #if married with no kids S=5 the max is 20
    # Function to calculate 'S' based on 'sit_fam' and 'NOMBRE_ENF'
    def calculate_S(row):
        sit_fam = row['sit_fam'].strip().lower()
        nbr_enf = row['NOMBRE_ENF']

        if sit_fam not in ['Célibataire']:
            if nbr_enf <= 3:
                return 5 + nbr_enf * 5
            else:
                return 20
        else:
            return 0  # Default to 0 for unknown cases

    # Calculate 'S' for each row in demandes_traiter_df
    demandes_traiter_df['S'] = demandes_traiter_df.apply(calculate_S, axis=1)

    # ## Calculate D

    # Create a function to calculate 'D' based on conditions
    def calculate_D(row, historique_df):
        matricule = row['Matricule']
        matricule_rows = historique_df[historique_df['Matricule'] == matricule]
        total_D = 0
        
        for index, hist_row in matricule_rows.iterrows():
            date_de_debut_sejour = hist_row['Date debut sejour']
            year_difference = datetime.now().year - date_de_debut_sejour.year
            
            if year_difference == 1:
                total_D += 140
            elif year_difference == 2:
                total_D += 90
            elif year_difference == 3:
                total_D += 50
            elif year_difference >= 4:
                total_D += 20
        
        return total_D

    # Calculate 'D' for each row in demandes_traiter_df using the calculate_D function
    demandes_traiter_df['D'] = demandes_traiter_df.apply(calculate_D, axis=1, historique_df=historique_df)

    # Fill NaN values with 0 in case there are Matricules in demandes_traiter_df that didn't occur in historique_df
    demandes_traiter_df['D'] = demandes_traiter_df['D'].fillna(0)




    # ## Calculate P 

    # Calculate 'P' based on the formula P = 2 * (A + S) - D
    demandes_traiter_df['P'] = 2 * (demandes_traiter_df['A'] + demandes_traiter_df['S']) - demandes_traiter_df['D']


    # ## Sorting based on 'P'

    # Sort demandes_traiter_df based on the 'P' column in descending order
    demandes_traiter_df = demandes_traiter_df.sort_values(by=['P', 'A', 'S','Date de la demande'], ascending=[False, False, False,False])
    print(demandes_traiter_df.columns)

    
    # Delete old records and save new records to the database
    DemandesTraiter.objects.all().delete()
    # Prepare data for saving into the database
    for index, row in demandes_traiter_df.iterrows():
        DemandesTraiter.objects.create(
            numero_demande=row['N° Demande'],
            ville=row['Ville'],
            nom_agent=row['Nom agent'],
            prenom_agent=row['Prenom agent'],
            matricule=row['Matricule'],
            date_debut_sejour=row['Date debut sejour'],
            date_fin_sejour=row['Date fin sejour'],
            type_de_vue=row['Type de vue'],
            A=row['A'],
            D=row['D'],
            S=row['S'],
            P=row['P'],
        )


 



from io import BytesIO
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def create_pdf(principal_data, waiting_data, col_widths, title_text, title_text_wait, filename='sorted_table.pdf'):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
    elements = []

    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        name='TitleStyle',
        fontName='Helvetica-Bold',
        fontSize=10,
        textColor=colors.black,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    normal_style = styles['Normal']
    normal_style.fontName = 'Helvetica'
    normal_style.fontSize = 10

    # Add title text as a Paragraph
    title_paragraph = Paragraph(title_text, title_style)
    elements.append(title_paragraph)
    elements.append(Spacer(1, 20))  # 20 points of space

    # Remove 'Type de vue' column from principal_data and waiting_data
    principal_data = [row for row in principal_data if row[0] != 'type_de_vue']
    waiting_data = [row for row in waiting_data if row[0] != 'type_de_vue']

    # Create principal table
    principal_table = Table(principal_data, colWidths=col_widths)
    principal_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.black),  # Header background color
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Header text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font style (bold)
        ('FONTSIZE', (0, 0), (-1, 0), 10),  # Font size for header row
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),  # Data rows background color
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),  # Adjust font size if necessary
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),  # Alternating row colors
        ('COLBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.lightgrey])  # Alternating column colors
    ])
    principal_table.setStyle(principal_style)
    elements.append(principal_table)
    elements.append(Spacer(1, 24))

    # Add message if waiting list is empty
    if len(waiting_data) <= 1:  # Check if waiting_data has only the header row
        empty_waiting_list_text = f"*{title_text_wait} est vide"
        empty_waiting_list_paragraph = Paragraph(empty_waiting_list_text, normal_style)
        elements.append(Spacer(1, 20))  # 20 points of space
        elements.append(empty_waiting_list_paragraph)
    else:
        # Add page break and title for waiting list
        elements.append(PageBreak())
        waiting_title_paragraph = Paragraph(title_text_wait, title_style)
        elements.append(waiting_title_paragraph)
        elements.append(Spacer(1, 20))  # 20 points of space

        # Create waiting list table
        waiting_table = Table(waiting_data, colWidths=col_widths)
        waiting_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.black),  # Header background color
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Header text color
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font style (bold)
            ('FONTSIZE', (0, 0), (-1, 0), 10),  # Font size for header row
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),  # Data rows background color
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),  # Adjust font size if necessary
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),  # Alternating row colors
            ('COLBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.lightgrey])  # Alternating column colors
        ])
        waiting_table.setStyle(waiting_style)
        elements.append(waiting_table)

    # Build the PDF
    doc.build(elements)
    pdf_data = buffer.getvalue()
    buffer.close()

    return pdf_data

def quota_list(request):
    quotas = Quota.objects.all()
    type_de_vue_list = Quota.objects.values_list('type_de_vue', flat=True).distinct()
    return render(request, 'listings/quota.html', {'quotas': quotas, 'type_de_vue_list': type_de_vue_list})



def update_quota(request):
    if request.method == 'POST':
        ville = request.POST.get('original_ville')
        type_de_vue = request.POST.get('original_type_de_vue')
        new_quota_value = request.POST.get('quota_value')
        
        quota = Quota.objects.get(ville=ville, type_de_vue=type_de_vue)
        quota.quota_value = new_quota_value
        quota.save()

    quotas = Quota.objects.all()
        
    return render(request, 'listings/quota.html', {'quotas': quotas}) # Redirect to the view showing the table

def delete_quota(request):
    if request.method == 'POST':
        ville = request.POST.get('ville')
        type_de_vue = request.POST.get('type_de_vue')
        
        Quota.objects.filter(ville=ville, type_de_vue=type_de_vue).delete()

    quotas = Quota.objects.all()
        
    return render(request, 'listings/quota.html', {'quotas': quotas})  # Redirect to the view showing the table

def add_quota(request):
    if request.method == 'POST':
        ville = request.POST.get('ville')
        type_de_vue = request.POST.get('type_de_vue')
        quota_value = request.POST.get('quota_value')
        
        # Create a new Quota record
        Quota.objects.create(ville=ville, type_de_vue=type_de_vue, quota_value=quota_value)
        
        

    quotas = Quota.objects.all()
        
    return render(request, 'listings/quota.html', {'quotas': quotas})

from django.shortcuts import render, redirect
from django.contrib import messages
import pandas as pd
from .models import Historique

def historique(request):
    # Display the page with the table and form
    historiques = Historique.objects.all()
    return render(request, 'listings/historique.html', {'historiques': historiques})

def upload_excel_historique(request):
    if request.method == 'POST':
        if 'excel_file' not in request.FILES:
            messages.error(request, "Aucun fichier Excel trouvé.")
            return redirect('historique')

        excel_file = request.FILES['excel_file']
        df = pd.read_excel(excel_file)

        # Clean the table before uploading new data
        Historique.objects.all().delete()

        # Validate columns
        required_columns = ['ville', 'nom_agent', 'prenom_agent', 'matricule',
                            'date_demande', 'date_debut_sejour', 'date_fin_sejour',
                            'type_de_vue', 'nombre_nuites']
        
       

        # Insert data into the database
        for _, row in df.iterrows():
            Historique.objects.create(
                ville=row['ville'],
                nom_agent=row['nom_agent'],
                prenom_agent=row['prenom_agent'],
                matricule=row['matricule'],
                date_demande=row['date_demande'],
                date_debut_sejour=row['date_debut_sejour'],
                date_fin_sejour=row['date_fin_sejour'],
                type_de_vue=row['type_de_vue'],
                nombre_nuites=row['nombre_nuites'],
            )
        
        messages.success(request, "Fichier Excel traité avec succès.")

    return redirect('historique')


def delete_historique(request):
    if request.method == 'POST':
        Historique.objects.all().delete()
        messages.success(request, "Toutes les données ont été supprimées.")
        
    return redirect('historique')
