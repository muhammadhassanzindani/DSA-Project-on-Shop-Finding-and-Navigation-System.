import pandas as pd

class Shop:
    def __init__(self, shop_id, shop_name, categories, location, rating):
        if not shop_id:
            raise ValueError("Shop ID should be alphanumeric and not empty.")
        self.shop_id = shop_id
        self.shop_name = shop_name
        self.categories = tuple(category.strip().capitalize() for category in categories.split(','))
        self.location = location
        self.rating = rating
        
        self.design = "*"*25

    def __str__(self):
        formatted_categories = ', '.join(self.categories)
        return f'{self.design}\n, Shop ID: {self.shop_id}\n, Shop Name: {self.shop_name}\n, Categories: {formatted_categories}\n, Location: {self.location}\n, Rating: {self.rating}\n, {self.design}'


# Hash Table Function
class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size
        self.secondary_hash_increment = 7  # Increment for secondary hash (should be relatively prime to the table size)

    def _hash(self, key):
        return hash(key) % self.size

    def _double_hash(self, key, i):
        return (self._hash(key) + i * self.secondary_hash_increment) % self.size

    def put(self, key, value):
        i = 0
        while i < self.size:
            index = self._double_hash(key, i)
            if self.table[index] is None:
                self.table[index] = [(key, value)]
                return True
            elif self.table[index][0][0] == key:
                self.table[index].append((key, value))
                return True
            i += 1
        return False

    def get(self, key):
        i = 0
        while i < self.size:
            index = self._double_hash(key, i)
            items = self.table[index]
            if items:
                for item in items:
                    if item[0] == key:
                        return item[1]
            i += 1
        return None

    def __delitem__(self, key):
        i = 0
        while i < self.size:
            index = self._double_hash(key, i)
            items = self.table[index]
            if items:
                self.table[index] = [item for item in items if item[0] != key]
            i += 1

    def delete_value(self, key, value):
        i = 0
        while i < self.size:
            index = self._double_hash(key, i)
            items = self.table[index]
            if items:
                self.table[index] = [(k, v) for k, v in items if k != key or v != value]
                if not self.table[index]:  # If the key is empty, delete it
                    self.__delitem__(key)
            i += 1

    def delete_key_if_empty(self, key):
        i = 0
        while i < self.size:
            index = self._double_hash(key, i)
            items = self.table[index]
            if items and all(item[0] != key for item in items):
                self.table[index] = None
            i += 1

    def get_keys(self):
        keys = [item[0][0] for item in self.table if item is not None]
        return keys

    def get_values(self):
        values = [item[0][1] for item in self.table if item is not None]
        return values

# Creating Own Heap Function
class Heap:
    def __init__(self):
        self.heap = []

    def push(self, item):
        self.heap.append(item)
        self._heapify_up(len(self.heap) - 1)

    def pop(self):
        if len(self.heap) == 0:
            raise IndexError("Heap is empty")
        
        if len(self.heap) == 1:
            return self.heap.pop()

        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return root

    def skip(self):  
        return None if len(self.heap) == 0 else self.heap[0]

    def _heapify_up(self, index):
        parent = (index - 1) // 2
        while index > 0 and self.heap[index] > self.heap[parent]:
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            index = parent
            parent = (index - 1) // 2

    def _heapify_down(self, index):
        left_child = 2 * index + 1
        right_child = 2 * index + 2
        largest = index

        if left_child < len(self.heap) and self.heap[left_child] > self.heap[largest]:
            largest = left_child

        if right_child < len(self.heap) and self.heap[right_child] > self.heap[largest]:
            largest = right_child

        if largest != index:
            self.heap[index], self.heap[largest] = self.heap[largest], self.heap[index]
            self._heapify_down(largest)

class MarketPlace:
    def __init__(self):
        self.adjacency_list = {}
        self.shop_info = {}  # Store shop information
        self.category_hash_table = HashTable(1000) # choose big size for better result
        self.category_max_heaps = {}  # Max heaps for each category
 
        # Reconstruct max heaps from existing shop information
        for shop_id, shop in self.shop_info.items():
            if shop.category not in self.category_max_heaps:
                self.category_max_heaps[shop.category] = Heap()

            self.category_max_heaps[shop.category].push((-shop.rating, shop_id))
            
        

    def add_shop(self, shop):
        if shop.shop_id in self.adjacency_list:
            print(f"Error: Shop with ID {shop.shop_id} already exists. Use a different shop ID.")
        else:
            self.adjacency_list[shop.shop_id] = []
            self.shop_info[shop.shop_id] = shop
            print(f"Shop with ID {shop.shop_id} added successfully.")

            # Handle single or multiple categories
            categories = shop.categories if isinstance(shop.categories, tuple) else tuple(shop.categories.split(','))   
            capitalized_categories = [category.strip().capitalize() for category in categories]

            # Update category hash table for each category of the shop
            for category in capitalized_categories:
                existing_values = self.category_hash_table.get(category)
                
                if existing_values is None:
                    existing_values = []  # If the category is not present, create an empty list
            
                # Check if the shop ID is not already in the list of values
                if shop.shop_id not in existing_values:
                    existing_values.append(shop.shop_id)
                    self.category_hash_table.put(category, existing_values)
                else:
                    print("Error: Unable to add the shop to the category hash table.")
            

    def add_edge(self, shop1_id, shop2_id):
        if shop1_id not in self.adjacency_list or shop2_id not in self.adjacency_list:
            print("Error: One or both shops do not exist.")
            return

        if shop2_id not in self.adjacency_list[shop1_id]:
            self.adjacency_list[shop1_id].append(shop2_id)
            self.adjacency_list[shop2_id].append(shop1_id)
            print(f"Edge added between Shop ID {shop1_id} and Shop ID {shop2_id}.")
        else:
            print(f"Error: Edge between Shop ID {shop1_id} and Shop ID {shop2_id} already exists.")

    def delete_edge(self, shop1_id, shop2_id):
        if shop1_id not in self.adjacency_list or shop2_id not in self.adjacency_list:
            print("Error: One or both shops do not exist.")
            return

        if shop2_id in self.adjacency_list[shop1_id]:
            self.adjacency_list[shop1_id].remove(shop2_id)
            self.adjacency_list[shop2_id].remove(shop1_id)
            print(f"Edge deleted between Shop ID {shop1_id} and Shop ID {shop2_id}.")
        else:
            print(f"Error: No edge exists between Shop ID {shop1_id} and Shop ID {shop2_id}.")

    def display_shop_info(self, shop_id):
        if shop_id in self.shop_info:
            print(self.shop_info[shop_id])
        else:
            print(f"Shop with ID {shop_id} does not exist.")

    def display_adjacency_list(self):
        print("Adjacency List:")
        for shop_id, connections in self.adjacency_list.items():
            print(f"Shop ID {shop_id} is connected to: {connections}")

    def delete_shop(self, shop_id):
        if shop_id in self.shop_info:
            # Get shop and category
            shop = self.shop_info[shop_id]
            category = shop.categories

            for neighbor_id in self.adjacency_list[shop_id]:
                self.adjacency_list[neighbor_id].remove(shop_id)
            del self.adjacency_list[shop_id]
            del self.shop_info[shop_id]
            print(f"Shop with ID {shop_id} deleted successfully.")

            # Update category hash table
            for single_cat in category:
                single_cat = single_cat.capitalize()
                
                if single_cat in self.category_hash_table.get_keys():
                    # Retrieve the list of shops associated with the category
                    existing_shops = self.category_hash_table.get(single_cat)
            
                    # Check if the shop_id is in the list of shops
                    if shop_id in existing_shops:
                        # Remove the shop from the list
                        existing_shops.remove(shop_id)
            
                        # Update the category in the HashTable with the updated list of shops
                        self.category_hash_table.put(single_cat, existing_shops)
            
                        # Remove the category if no shops are left
                        if not existing_shops:
                            self.category_hash_table.delete_key_if_empty(single_cat)
                    else:
                        print(f"Error: Shop with ID {shop_id} does not exist in the category {single_cat}.")
                else:
                    print(f"Error: Category {single_cat} does not exist in the category hash table.")



    def update_shop(self, shop_id):
        if shop_id in self.shop_info:
            shop = self.shop_info[shop_id]
            print("Current shop information:")
            print(shop)
            
            shop_name = input(f"Enter new shop name (current: {shop.shop_name}, press Enter to keep): ").capitalize()
            new_categories = input(f"Enter new shop categories (current: {', '.join(shop.categories)}, press Enter to keep, separated by commas): ")
            new_categories = tuple(category.strip().capitalize() for category in new_categories.split(','))
            new_location = input(f"Enter new shop location (current: {shop.location}, press Enter to keep): ").capitalize()
            new_rating = float(input(f"Enter new shop rating (current: {shop.rating}, press Enter to keep): ") or shop.rating)
    
            # Update category information and move shop to the new category
            self.update_shop_category(shop_id, ', '.join(new_categories))
    
            # Update the shop's information
            shop.shop_name = shop_name
            shop.location = new_location if new_location else shop.location
            shop.rating = new_rating
            shop.categories = new_categories
    
            self.shop_info[shop_id] = shop
            print("The shop has been updated successfully")
        
        else:
            print(f"Error: Shop with ID {shop_id} does not exist.")

    def update_shop_category(self, shop_id, new_categories):
        # Convert new categories to a list of capitalized categories
        new_categories_list = [category.strip().capitalize() for category in new_categories.split(',')]
    
        # Get the shop
        shop = self.shop_info[shop_id]
    
        # Remove the shop from the old categories and delete empty categories
        for old_category in shop.categories:
            old_category = old_category.capitalize()
            if shop_id in self.category_hash_table.get(old_category):
                self.category_hash_table.delete_value(old_category, shop_id)
                if not self.category_hash_table.get(old_category):
                    self.category_hash_table.delete_key_if_empty(old_category)
    
        # Update the shop's categories
        shop.categories = new_categories_list
    
        # Add the shop to the new categories
        for category in new_categories_list:
            category = category.capitalize()
            if category not in self.category_hash_table.get_keys():
                self.category_hash_table.put(category, [shop_id])
            else:
                existing_shops = self.category_hash_table.get(category)
                if shop_id not in existing_shops:
                    existing_shops.append(shop_id)
                    self.category_hash_table.put(category, existing_shops)

            
    def display_all_shops(self):
        print("\nAll Shops:")
        for shop_id, shop in self.shop_info.items():
            print(shop)

    def dfs(self, start_shop, end_shop, visited, path):
        visited[start_shop] = True
        path.append(start_shop)

        if start_shop == end_shop:
            return path

        for neighbor in self.adjacency_list[start_shop]:
            if not visited[neighbor]:
                if new_path := self.dfs(neighbor, end_shop, visited, path):
                    return new_path

        path.pop()
        return None

    def bfs(self, start_shop, end_shop):
        visited = {shop: False for shop in self.adjacency_list}
        queue = [[start_shop]]

        while queue:
            path = queue.pop(0)
            node = path[-1]

            if node == end_shop:
                return path

            for neighbor in self.adjacency_list[node]:
                if not visited[neighbor]:
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)
                    visited[neighbor] = True

        return None
    
    def display_dfs(self, start_shop, end_shop):
        if start_shop not in self.adjacency_list or end_shop not in self.adjacency_list:
            print("Error: One or both shops do not exist.")
            return

        print(f"\nFinding path from Shop ID {start_shop} to Shop ID {end_shop} using DFS:")
        if dfs_path := self.dfs(start_shop, end_shop, {shop: False for shop in self.adjacency_list}, []):
            print("DFS Path:", dfs_path)
            print("DFS Path Length:", len(dfs_path) - 1)
        else:
            print("No valid path using DFS.")

    def display_bfs(self, start_shop, end_shop):
        if start_shop not in self.adjacency_list or end_shop not in self.adjacency_list:
            print("Error: One or both shops do not exist.")
            return

        print(f"\nFinding path from Shop ID {start_shop} to Shop ID {end_shop} using BFS:")
        bfs_path = self.bfs(start_shop, end_shop)
        if bfs_path:
            print("BFS Path:", bfs_path)
            print("BFS Path Length:", len(bfs_path) - 1)
        else:
            print("No valid path using BFS.")

    def find_path(self, start_shop, end_shop):
        if start_shop not in self.adjacency_list or end_shop not in self.adjacency_list:
            print("Error: One or both shops do not exist.")
            return

        print(f"\nFinding path from Shop ID {start_shop} to Shop ID {end_shop} using DFS:")
        dfs_path = self.dfs(start_shop, end_shop, {shop: False for shop in self.adjacency_list}, [])
        
        if dfs_path:
            print("DFS Path:", dfs_path)
            print("DFS Path Length:", len(dfs_path) - 1)
        else:
            print("No valid path using DFS.")

        print(f"\nFinding path from Shop ID {start_shop} to Shop ID {end_shop} using BFS:")
        bfs_path = self.bfs(start_shop, end_shop)
        
        if bfs_path:
            print("BFS Path:", bfs_path)
            print("BFS Path Length:", len(bfs_path) - 1)
        else:
            print("No valid path using BFS.")

        shortest_path = None
        shortest_length = float('inf')
        if dfs_path and len(dfs_path) - 1 < shortest_length:
            shortest_path = dfs_path
            shortest_length = len(dfs_path) - 1
            
        if bfs_path and len(bfs_path) - 1 < shortest_length:
            shortest_path = bfs_path
            shortest_length = len(bfs_path) - 1

        if shortest_path:
            print("\nShortest Path:", shortest_path)
            print("Shortest Path Length:", shortest_length)
        else:
            print("No valid path found.")
            
    def compare_paths(self, start_shop, end_shop):
        if start_shop not in self.adjacency_list or end_shop not in self.adjacency_list:
            print("Error: One or both shops do not exist.")
            return

        dfs_path = self.dfs(start_shop, end_shop, {shop: False for shop in self.adjacency_list}, [])
        bfs_path = self.bfs(start_shop, end_shop)

        print("\nComparison of DFS and BFS Paths:\n")
        print(f"DFS Path: {dfs_path or 'No valid path using DFS.'}")
        print(f"BFS Path: {bfs_path or 'No valid path using BFS.'}")

        if dfs_path and bfs_path:
            if len(dfs_path) < len(bfs_path):
                print("DFS provides the shortest path.")
            elif len(bfs_path) < len(dfs_path):
                print("BFS provides the shortest path.")
            else:
                print("DFS and BFS paths have the same length.")
                

    def display_categories(self):
        categories = self.category_hash_table.get_keys()
        print("\nCategories:")
        for idx, category in enumerate(categories, start=1):
            print(f"{idx}. {category.capitalize()}")  # Ensure proper capitalization
    
        return categories

  
    def display_shops_by_category(self, selected_category):
        selected_category = selected_category.strip().capitalize()  # Ensure proper capitalization
    
        if selected_category in self.category_hash_table.get_keys():
            print(f"\nShops in the category '{selected_category}':")
            shop_ids = self.category_hash_table.get(selected_category)
    
            for shop_id in shop_ids:
                shop = self.shop_info.get(shop_id)
    
                if shop:
                    print(shop)
        else:
            print(f"No shops found in the category '{selected_category}'.")
            
            
    def display_shops_by_category_sorted(self, selected_category):
        selected_category = selected_category.strip().capitalize()  # Ensure proper capitalization
    
        if selected_category in self.category_hash_table.get_keys():
            while True:
                print(f"\nShops in the category '{selected_category}':")
                print("1. Higher to Lower")
                print("2. Lower to Higher")
                sort_choice = input("Enter your sorting choice (1 or 2): ")
    
                if sort_choice == '1':
                    descending = False  # Sort in ascending order
                    break
                elif sort_choice == '2':
                    descending = True  # Sort in descending order
                    break
                else:
                    print("Invalid sorting choice. Please enter 1 or 2.")
    
            shops = [
                (shop, -shop.rating) for shop_id, shop in self.shop_info.items() if
                shop_id in self.category_hash_table.get(selected_category)
            ]
            shops.sort(key=lambda x: x[1], reverse=descending)
    
            for shop, rating in shops:
                print(shop)
        else:
            print(f"No shops found in the category '{selected_category}'.")
            
    def load_data_from_excel(market_space, excel_file):
        shop_info_sheet = "Shops info"
        edges_sheet = "Edges"

        # Load shop information from the "Shop Info" sheet
        shop_info_data = pd.read_excel(excel_file, sheet_name=shop_info_sheet)
        for index, row in shop_info_data.iterrows():
            shop_id = str(row['Shop Number'])
            shop_name = row['Shop Name']
            categories = row['Category']
            location = row['Location']
            rating = float(row['Rating'])
            new_shop = Shop(shop_id, shop_name, categories, location, rating)
            market_space.add_shop(new_shop)

        # Load edges from the "Edges" sheet
        edges_data = pd.read_excel(excel_file, sheet_name=edges_sheet)
        for index, row in edges_data.iterrows():
            shop1_id = str(row['Source shop'])
            shop2_id = str(row['Destination shop'])
            market_space.add_edge(shop1_id, shop2_id)


def main():
    market_space = MarketPlace()
    excel_file = "test_file.xlsx"  # Replace with your Excel file path

    # Load data from the Excel file
    MarketPlace.load_data_from_excel(market_space, excel_file)

    while True:
        print("\n>>>>>>>>>> Shop Finding and Navigation System <<<<<<<<<<")
        print("\nMenu:")
        print("1. Display Adjacency List")
        print("2. Add a Shop")
        print("3. Delete a Shop")
        print("4. Update Shop Information")
        print("5. Display Shop Information")
        print("6. Show all shops")
        print("7. Add Edge (Connection between Shops)")
        print("8. Delete Edge (Connection between Shops)")
        print("9. Display DFS Path")
        print("10. Display BFS Path")
        print("11. Compare DFS and BFS Paths")
        print("12. Find shortest Path from Source to Destination")
        print("13. Search Shop by Category")
        print("14. Search Shop by Rating")
        print("15. Exit")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            market_space.display_adjacency_list()
            
        elif choice == '2':
            try:
                shop_id = input("Enter the Shop ID: ")
                shop_name = input("Enter the Shop Name: ")
                categories = input("Enter the Shop Categories (separated by commas): ")
                location = input("Enter the Shop Location: ")
                rating = float(input("Enter the Shop Rating (1-5): "))
                new_shop = Shop(shop_id, shop_name, categories, location, rating)
                market_space.add_shop(new_shop)
            except ValueError as e:
                print(f"Error: {str(e)}")
        elif choice == '3':
            try:
                shop_id = input("Enter the Shop ID to delete: ")
                market_space.delete_shop(shop_id)
            except ValueError as e:
                print(f"Error: {str(e)}")
        
        elif choice == '4':
            try:
                shop_id = input("Enter the Shop ID to update: ")
                market_space.update_shop(shop_id)
            except ValueError as e:
                print(f"Error: {str(e)}")
        
        elif choice == '5':
            try:
                shop_id = input("Enter the Shop ID to display information: ")
                market_space.display_shop_info(shop_id)
            except ValueError as e:
                print(f"Error: {str(e)}")
                
        elif choice == '6':
            market_space.display_all_shops()
        
        elif choice == '7':
            try:
                shop1_id = input("Enter the first Shop ID for the edge: ")
                shop2_id = input("Enter the second Shop ID for the edge: ")
                market_space.add_edge(shop1_id, shop2_id)
            except ValueError as e:
                print(f"Error: {str(e)}")
        
        elif choice == '8':
            try:
                shop1_id = input("Enter the first Shop ID for the edge to delete: ")
                shop2_id = input("Enter the second Shop ID for the edge to delete: ")
                market_space.delete_edge(shop1_id, shop2_id)
            except ValueError as e:
                print(f"Error: {str(e)}")
                
        elif choice == '9':
            try:
                source_shop = input("Enter the source Shop ID: ")
                destination_shop = input("Enter the destination Shop ID: ")
                market_space.display_dfs(source_shop, destination_shop)
            except ValueError as e:
                print(f"Error: {str(e)}")

        elif choice == '10':
            try:
                source_shop = input("Enter the source Shop ID: ")
                destination_shop = input("Enter the destination Shop ID: ")
                market_space.display_bfs(source_shop, destination_shop)
            except ValueError as e:
                print(f"Error: {str(e)}")
                
        elif choice == '11':
            try:
                source_shop = input("Enter the source Shop ID: ")
                destination_shop = input("Enter the destination Shop ID: ")
                market_space.compare_paths(source_shop, destination_shop)
            except ValueError as e:
                print(f"Error: {str(e)}")
        
        elif choice == '12':
            try:
                source_shop = input("Enter the source Shop ID: ")
                destination_shop = input("Enter the destination Shop ID: ")
                market_space.find_path(source_shop, destination_shop)
            except ValueError as e:
                print(f"Error: {str(e)}")
        
        elif choice == '13':
            categories = market_space.display_categories()
            if categories:
                try:
                    category_choice = int(input("Enter the number of the desired category: "))
                    if 1 <= category_choice <= len(categories):
                        selected_category = categories[category_choice - 1]
                        market_space.display_shops_by_category(selected_category)
                    else:
                        print("Invalid category choice. Please try again.")
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
                    
        elif choice == '14':
            categories = market_space.category_hash_table.get_keys()
            if categories:
                print("\nCategories:")
                for i, category in enumerate(categories, start=1):
                    print(f"{i}. {category.capitalize()}")
            
                try:
                    selected_category_num = int(input("\nEnter the number of the desired category: "))
                    if 1 <= selected_category_num <= len(categories):
                        selected_category = categories[selected_category_num - 1]
                        market_space.display_shops_by_category_sorted(selected_category)
                    else:
                        print("Invalid category number.")
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
            else:
                print("No categories found in the category hash table.")
            
        elif choice == '15':
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()

