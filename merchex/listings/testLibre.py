import pandas as pd

from .models import AgentsLibre

def get_filtered_agents(ville, type_de_vue):
    return AgentsLibre.objects.filter(ville=ville, type_de_vue=type_de_vue)

def process_excel_file(file):
    df = pd.read_excel(file)
    return df


def optimize_assignment(agents_df, chalets_df):
    # Implémentez votre algorithme d'optimisation ici
    # Exemple simplifié : affecter les agents de manière aléatoire
    assignments = {}
    chalets = chalets_df['Chalet'].tolist()
    for i, agent in agents_df.iterrows():
        if chalets:
            chalet = chalets.pop(0)
            assignments[agent['matricule']] = chalet
    return assignments


from django.http import HttpResponse
from django.views import View

class ProcessDataView(View):
    def post(self, request, *args, **kwargs):
        ville = request.POST.get('ville')
        type_de_vue = request.POST.get('type_de_vue')
        excel_file = request.FILES['chalets_file']

        # Filtrer les agents
        agents = get_filtered_agents(ville, type_de_vue)
        agents_df = pd.DataFrame(list(agents.values()))

        # Lire les données des chalets
        chalets_df = process_excel_file(excel_file)

        # Optimiser l'affectation
        assignments = optimize_assignment(agents_df, chalets_df)

        # Générer le fichier de résultats
        output_path = '/path/to/output/optimized_assignments.xlsx'
        generate_result_file(assignments, output_path)

        # Envoyer le fichier au client
        with open(output_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename="optimized_assignments.xlsx"'
            return response
        

def affecter():
    ville="Marrakech"
    type_de_vue=""
    filtred_agents=AgentsLibre.objects.filter(ville=ville, type_de_vue=type_de_vue)
    df = pd.read_excel('D:\OCP_Social_Stage\vue.xslx', engine='openpyxl')
    assignments = {}
    chalets = df['Chalet'].tolist()
    for i, agent in filtred_agents.iterrows():
        if chalets:
            chalet = chalets.pop(0)
            assignments[agent['matricule']] = chalet
    print(assignments)
    return assignments



#solution 1


def affecter(request, ville, type_de_vue):
    if request.method == 'POST':
        form = AffectationForm(request.POST, request.FILES)
        print("1")
        
        if form.is_valid():
            print("2")
            aff_file = request.FILES.get('affectation_file')
            print("File received:", aff_file)

            # Filtrer les agents en fonction de la ville et du type de vue
            filtred_agents = AgentsLibre.objects.filter(ville=ville, type_de_vue=type_de_vue)

            # Charger le fichier Excel fourni sans en modifier la structure
            workbook = load_workbook(aff_file)
            worksheet = workbook.active

            # Dictionnaire pour suivre les affectations
            assignments = {}

            # Itérer sur les agents filtrés pour les affecter aux chalets et périodes disponibles
            for agent in filtred_agents:
                assigned = False
                for row in range(4, worksheet.max_row + 1):  # Parcourir les lignes des chalets
                    chalet = worksheet.cell(row=row, column=2).value  # Colonne B contient les chalets

                    if chalet:
                        start_day = agent.date_debut_sejour.day
                        end_day = agent.date_fin_sejour.day
                        period_available = True

                        # Vérifier si la période souhaitée est libre pour ce chalet
                        for day in range(start_day, end_day + 1):
                            if worksheet.cell(row=row, column=day + 2).value:  # +2 pour ajuster l'index de la colonne
                                period_available = False
                                break

                        # Si la période est disponible, affecter l'agent
                        if period_available:
                            for day in range(start_day, end_day + 1):
                                worksheet.cell(row=row, column=day + 2).value = agent.matricule
                            assignments[agent.matricule] = chalet
                            assigned = True
                            break

                # Si l'agent n'a pas pu être affecté, il est ignoré
                if not assigned:
                    print(f"Agent {agent.matricule} non affecté à cause d'un manque de période disponible.")

            # Sauvegarder le fichier Excel dans un objet BytesIO pour l'envoi en tant que réponse HTTP
            output = BytesIO()
            workbook.save(output)
            output.seek(0)

            # Préparer la réponse HTTP avec le fichier Excel en pièce jointe
            response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename="Affectation_{ville}_{type_de_vue}.xlsx"'

            return response
        
        else:
            # Afficher les erreurs du formulaire pour débogage
            print("Form errors:", form.errors)
    return redirect('libres_files')




#solution 2 minimisation gap


def affecter(request, ville, type_de_vue):
    if request.method == 'POST':
        form = AffectationForm(request.POST, request.FILES)
        if form.is_valid():
            aff_file = request.FILES.get('affectation_file')
            filtred_agents = AgentsLibre.objects.filter(ville=ville, type_de_vue=type_de_vue)
            workbook = load_workbook(aff_file)
            worksheet = workbook.active
            assignments = {}

            for agent in filtred_agents:
                assigned = False
                possible_assignments = []

                for row in range(4, worksheet.max_row + 1):
                    chalet = worksheet.cell(row=row, column=2).value
                    if not chalet:
                        continue

                    start_day = agent.date_debut_sejour.day
                    end_day = agent.date_fin_sejour.day
                    gap_minimum = None
                    period_available = True
                    gap_available = False
                    open_right = False
                    open_left = False

                    # Vérification si la période est disponible
                    for day in range(start_day, end_day + 1):
                        if worksheet.cell(row=row, column=day + 2).value:
                            period_available = False
                            break

                    if period_available:
                        # Vérification des ouvertures et calcul du gap
                        for day in range(3, 34):
                            if worksheet.cell(row=row, column=day).value:
                                if day + 1 <= 33 and not worksheet.cell(row=row, column=day + 1).value:
                                    open_right = True
                                if day - 1 >= 3 and not worksheet.cell(row=row, column=day - 1).value:
                                    open_left = True
                        gap_minimum = calculate_gap(worksheet, row, start_day, end_day)

                        if gap_minimum is not None:
                            gap_available = True

                        # Enregistrer les affectations possibles
                        possible_assignments.append((row, gap_minimum, open_right, open_left, gap_available))

                # Priorisation des affectations
                if possible_assignments:
                    possible_assignments.sort(
                        key=lambda x: (
                            -x[4],  # Prioriser les gaps disponibles (True > False)
                            x[1] if x[1] is not None else float('inf'), # Taille du gap minimum (minimiser le gap)
                            -x[2],  # Prioriser les ouvertures à droite (True > False)
                            -x[3],  # Prioriser les ouvertures à gauche (True > False)
                            not (x[2] or x[3])  # Enfin, affecter les chalets totalement libres (False > True)
                        )
                    )
                    selected_assignment = possible_assignments[0]
                    selected_row = selected_assignment[0]

                    # Affecter l'agent au chalet sélectionné
                    for day in range(start_day, end_day + 1):
                        worksheet.cell(row=selected_row, column=day + 2).value = agent.matricule

                    assignments[agent.matricule] = worksheet.cell(row=selected_row, column=2).value
                    assigned = True

                if not assigned:
                    print(f"Agent {agent.matricule} non affecté à cause d'un manque de période disponible.")

            output = BytesIO()
            workbook.save(output)
            output.seek(0)

            response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename="Affectation_{ville}_{type_de_vue}.xlsx"'

            return response
        
        else:
            print("Form errors:", form.errors)
    return redirect('libres_files')

def calculate_gap(worksheet, row, start_day, end_day):
    previous_filled = None
    next_filled = None

    for day in range(3, start_day):
        if worksheet.cell(row=row, column=day).value:
            previous_filled = day
            break

    for day in range(end_day + 1, 34):
        if worksheet.cell(row=row, column=day).value:
            next_filled = day
            break

    if previous_filled and next_filled:
        return min(next_filled - end_day, start_day - previous_filled)
    elif previous_filled:
        return start_day - previous_filled
    elif next_filled:
        return next_filled - end_day
    else:
        return None
