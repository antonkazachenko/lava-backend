# import pandas as pd
#
# df = pd.read_csv('./website_classification.csv')
#
# #['Travel' 'Social Networking and Messaging' 'News' 'Streaming Services'
#  # 'Sports' 'Photography' 'Law and Government' 'Health and Fitness' 'Games'
#  # 'E-Commerce' 'Forums' 'Food' 'Education' 'Computers and Technology'
#  # 'Business/Corporate' 'Adult']
#
# mapping = {
#     "Travel": 24,
#     "Social Networking and Messaging": 8,
#     "News": 14,
#     "Streaming Services": 7,
#     "Sports": 22,
#     "Photography": 2,
#     "Law and Government": 4,
#     "Health and Fitness": 22,
#     "Games": 12,
#     "E-Commerce": 10,
#     "Forums": 7,
#     "Food": 11,
#     "Education": 5,
#     "Computers and Technology": 6,
#     "Business/Corporate": 10,
#     "Adult": 1
# }
# df['Category'] = df['Category'].replace(mapping)
#
# print(df['Category'].unique())