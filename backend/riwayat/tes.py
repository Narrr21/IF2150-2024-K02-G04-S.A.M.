from riwayatManager import RiwayatManager

def print_menu():
    print("\nAvailable methods to test:")
    print("1. Add Riwayat")
    print("2. Get All Riwayat")
    print("3. Exit")
    print("\nChoose a method to test (1-3):", end=" ")

def test_add_riwayat(manager):
    print("\n=== Testing Add Riwayat ===")
    try:
        value = int(input("Enter value: "))
        action_code = input("Enter actionCode: ")
        success = input("Enter success (true/false): ").lower() == "true"
        
        manager.add_riwayat(value, action_code, success)
        print("\nRiwayat added !")
    except Exception as e:
        print(f"\nError : {e}")

def test_get_all_riwayat(manager):
    print("\n=== Testing Get All Riwayat ===")
    try:
        [success, riwayat_list, _]= manager.get_all_riwayat()
        # print(riwayat_list)
        if success:
            for riwayat in riwayat_list:
                riwayat.display()
        else:
            print("\nNo Riwayat found.")
    except Exception as e:
        print(f"\nError : {e}")

def main():
    manager = RiwayatManager()
    
    while True:
        print_menu()
        try:
            pilihan = input()
            if pilihan == "1":
                test_add_riwayat(manager)
            elif pilihan == "2":
                test_get_all_riwayat(manager)
            elif pilihan == "3":
                print("\nExit")
                break
            else:
                print("\nInvalid")
            
            cont = input("\ntest again ? (y/n): ").lower()
            if cont == 'n':
                print("\nExit")
                break
                
        except Exception as e:
            print(f"\nerror : {str(e)}")
            cont = input("\ntest again ? (y/n): ").lower()
            if cont == 'n':
                print("\nExit")
                break

if __name__ == "__main__":
    main()