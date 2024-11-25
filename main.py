import sqlite3
from datetime import datetime
from libs.sql_handler import (
    _checkDbExists, addUser, removeUser, addExercise, removeExercise, getExercises,
    getExerciseById, updateExercise, attributeExercise, createCategory, removeCategory
)

def main_menu():
    print("===== GESTÃO DE EXERCÍCIOS =====")
    print("1. Adicionar Usuário")
    print("2. Remover Usuário")
    print("3. Adicionar Exercício")
    print("4. Remover Exercício")
    print("5. Listar Exercícios")
    print("6. Ver Detalhes de um Exercício")
    print("7. Atualizar Exercício")
    print("8. Atribuir Exercício a Usuário")
    print("9. Criar Categoria de Exercício")
    print("10. Remover Categoria de Exercício")
    print("0. Sair")
    print("===============================")

def run():

    while True:
        main_menu()
        try:
            choice = int(input("Escolha uma opção: "))
        except ValueError:
            print("Opção inválida. Por favor, insira um número.")
            continue

        if choice == 1:
            name = input("Nome do Usuário: ")
            birthdate = input("Data de Nascimento (YYYY-MM-DD): ")
            weight = float(input("Peso (kg): "))
            height = float(input("Altura (m): "))
            addUser((name, birthdate, weight, height))
            print("Usuário adicionado com sucesso!")

        elif choice == 2:
            user_id = int(input("ID do Usuário a ser removido: "))
            result = removeUser(user_id)
            print(result)

        elif choice == 3:
            name = input("Nome do Exercício: ")
            description = input("Descrição: ")
            category_id = int(input("ID da Categoria: "))
            list_parent = int(input("ID da Lista de Exercícios (parent): "))
            series = int(input("Número de Séries: "))
            reps = int(input("Número de Repetições: "))
            weight = float(input("Peso (kg): "))
            addExercise((name, description, category_id, list_parent, series, reps, weight))
            print("Exercício adicionado com sucesso!")

        elif choice == 4:
            exercise_id = int(input("ID do Exercício a ser removido: "))
            result = removeExercise(exercise_id)
            print(result)

        elif choice == 5:
            exercises = getExercises()
            if exercises == "ERROR":
                print("Erro ao buscar exercícios.")
            else:
                for exercise in exercises:
                    print(f"Exercício ID: {exercise[0]}")
        
        elif choice == 6:
            exercise_id = int(input("ID do Exercício: "))
            details = getExerciseById(exercise_id)
            if details == "ERROR":
                print("Erro ao buscar detalhes do exercício.")
            else:
                print(details)

        elif choice == 7:
            exercise_id = int(input("ID do Exercício a ser atualizado: "))
            to_change = []
            while True:
                field = input("Digite o campo para alterar (name, description, etc.) ou 'sair' para finalizar: ")
                if field.lower() == "sair":
                    break
                value = input(f"Novo valor para {field}: ")
                to_change.append({field: value})
            result = updateExercise(exercise_id, to_change)
            print(result)
        
        elif choice == 8:
            exercise_id = int(input("ID do Exercício: "))
            user_id = int(input("ID do Usuário: "))
            result = attributeExercise(exercise_id, user_id)
            print(result)

        elif choice == 9:
            category_name = input("Nome da Categoria: ")
            result = createCategory((category_name,))
            print(result)

        elif choice == 10:
            category_id = int(input("ID da Categoria a ser removida: "))
            result = removeCategory(category_id)
            print(result)
        
        elif choice == 0:
            print("Saindo do programa.")
            break

        else:
            print("Opção inválida. Tente novamente.")
        print("\n")

if __name__ == "__main__":
    run()
