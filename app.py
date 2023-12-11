import pandas as pd
import eel
from apriory_backup import *
eel.init("web")

@eel.expose
def search(user_input_items):
    Apriory,plist = test(user_input_items)

    result = {
        "Apriory":list(Apriory),
        "ListKeys":list(plist),
        "List":plist
    }
    return result

class KMeansCluster:
    def __init__(self):
        self.clusters = []
        self.w2 = []
        
    def steps(self, data, clp):
        cl = len(clp)
        results = []
        print("\nInitial Cluster Points:", clp)  

        iteration = 0
        self.assigned_elements = {i: [] for i in range(1, cl + 1)}  

        while True: 

            print("\nIteration:", iteration + 1)
            
            dist_dict = []
            for i in range(cl):
                cluster_distances = []
                for j in range(len(data)):
                    c_diff = abs(float(clp[i]) - float(data[j]))
                    cluster_distances.append(c_diff)
                dist_dict.append(cluster_distances)
            
            print("Cluster points:", [f'{point:.4f}' for point in clp])
            print("Data and their differences between cluster points:")
            for j in range(len(data)):
                print("Data =", data[j], end=' ')
                for k2 in range(cl):
                    print(f"c{k2 + 1} = {dist_dict[k2][j]}", end=' ')
                print()
            
            w = []
            for j in range(len(data)):
                distances = [dist_dict[i][j] for i in range(cl)]
                min_distance = min(distances)
                cluster_index = distances.index(min_distance)
                w.append(cluster_index + 1)
                
                self.assigned_elements[cluster_index + 1].append(data[j])  

            
            print("Assigned clusters:", w)
            
            new_clp = []
            for cluster_index in range(1, cl + 1):
                cluster_points = [data[j] for j in range(len(data)) if w[j] == cluster_index]
                if cluster_points:
                    mean = sum(cluster_points) / len(cluster_points)
                    new_clp.append(mean)
            
            print("Updated cluster points:", [f'{point:.4f}' for point in new_clp])

            
            results.append(f"Iteration {iteration + 1}")
            results.append(f"Cluster points: {clp}")
            results.append(f"Assigned clusters: {w}")
            
            for i in range(1, cl + 1):
                self.assigned_elements[i] = [data[j] for j in range(len(data)) if w[j] == i]
            
            if new_clp == clp:
                break
            
            clp = new_clp
                    
            iteration += 1
            
        print("Final Clusters with their elements:")
        for i in range(1, cl + 1):
            print(f"Cluster {i} contains: {self.assigned_elements[i]}")
        
        self.w2 = w
        results.append("Final Clusters with their elements:")
        for i in range(1, cl + 1):
            results.append(f"Cluster {i} contains: {self.assigned_elements[i]}")
        return results


class ProductRecommendation:
    def __init__(self):
        self.data = pd.read_csv('pharmaproducts.csv')
        self.kmeans = KMeansCluster()

    def get_product_cluster(self, product_name):
        product_price = self.data[self.data['ProductName'] == product_name]['Price'].values
        print(product_price)
        if len(product_price) == 0:
            return None  
        product_price = product_price[0]
        
        for cluster, prices in self.kmeans.assigned_elements.items():
            if product_price in prices:
                print(cluster)
                return cluster  
        return None  

    def recommend_products_in_cluster(self, product_name):
        product_price = self.get_product_cluster(product_name)
        print(product_price)
        if product_price is not None:
            recommended_products = []
            for price in self.kmeans.assigned_elements[int(product_price)]:  
                if price != product_price:
                    recommended_product_names = self.data[self.data['Price'] == price]['ProductName'].values
                    recommended_products.extend(recommended_product_names)
            recommended_products = [product for product in recommended_products if product != product_name]  
            return recommended_products
        else:
            return []

product_recommendation = ProductRecommendation()

def datacleaning():
    data = pd.read_csv('Products.csv')

    missing_values = data.isnull().sum()

    data = data.dropna()

    duplicates = data.duplicated().sum()
    data = data.drop_duplicates()

    data.to_csv('pharmaproducts.csv', index=False)

@eel.expose
def perform_kmeans(num_clusters, cluster_points):
    data = pd.read_csv('pharmaproducts.csv')['Price'].tolist()
    product_recommendation.kmeans.clusters = [float(point) for point in cluster_points]
    results = product_recommendation.kmeans.steps(data, product_recommendation.kmeans.clusters)
    return results

@eel.expose
def search_products(product_name):
    recommended_products = product_recommendation.recommend_products_in_cluster(product_name)
    print(recommended_products)
    return recommended_products

eel.start("home.html",mode="default")

