import csv
from apyori import apriori

def test(user_input):
    with open('medicine_transaction_data.csv', 'r') as file:
        reader = csv.reader(file)
        data = list(reader)

    results = list(apriori(data,min_support=0.2, min_confidence=0.5,min_lift=1.0))
    print(results)

    print("Most Frequent Itemsets:")
    len_x = []
    for itemset in results:
        tem = list(itemset.items)
        if len(tem) > len(len_x):
            len_x = tem
    print(len_x)

    user_input_items = user_input.strip().split(',')

    # Print the association rules that match the user input
    print("\nAssociation Rules:")
    a = []
    plist = {}
    for itemset in results:
        if set(user_input_items).issubset(itemset.items):
            for rule in itemset.ordered_statistics:
                b = rule.items_base
                if len(rule.items_base) > 0:
                    for i in rule.items_base:
                        a.append(i)
                c = rule.items_add
                if len(rule.items_add) > 0:
                    for i in rule.items_add:
                        a.append(i)

                # Print support, lift, and confidence
                support = itemset.support
                lift = rule.lift
                confidence = rule.confidence

                # print(f"{', '.join(rule.items_base)} -> {', '.join(rule.items_add)}")
                # print(f"Support: {support}")
                # print(f"Lift: {lift}")
                # print(f"Confidence: {confidence}")
                # print("==")
                # print(type(', '.join(rule.items_base)))
            plist [', '.join(rule.items_base) + ',=>'+ ', ' + ', '.join(rule.items_add)] = []
            plist [', '.join(rule.items_base) + ',=>'+ ', ' + ', '.join(rule.items_add)]. append(f"Support: {support}")
            plist [', '.join(rule.items_base) + ',=>'+ ', ' + ', '.join(rule.items_add)]. append(f"Lift: {lift}\n")
            plist [', '.join(rule.items_base) + ',=>'+ ', ' + ', '.join(rule.items_add)]. append(f"Confidence: {confidence}\n")

    print("==")
    print(set(a))
    print(plist)

    return(set(a),plist)


# test()