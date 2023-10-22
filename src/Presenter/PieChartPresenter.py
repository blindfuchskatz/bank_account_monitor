

# from typing import Dict
# from src.Presenter.TransactionPresenter import TransactionPresenter
# from src.Sort.TransactionDict import TransactionDict
# import matplotlib.pyplot as plt


# class PiChartPresenter(TransactionPresenter):

#     def present(self, transaction_dict: TransactionDict) -> None:
#         plot_dict = {}

#         savings = 0

#         for category, transaction_list in transaction_dict.items():
#             if category == "Sparfound":
#                 continue
#             savings += self.__calcSum(transaction_list)

#         plot_dict["Savings"] = savings

#         for category, transaction_list in transaction_dict.items():

#             if self.__calcSum(transaction_list) > 0 or category == "Sparfound":
#                 continue
#             plot_dict[category] = abs(self.__calcSum(transaction_list))

#         labels = plot_dict.keys()
#         sizes = plot_dict.values()

#         # Create a pie chart
#         plt.figure(figsize=(6, 6))  # Set the size of the pie chart
#         plt.pie(sizes, labels=labels,
#                 autopct=lambda p: f'{p * sum(sizes) / 10000:.2f}', startangle=140)
#         # Equal aspect ratio ensures that the pie is drawn as a circle.
#         plt.axis('equal')

#         # Set a title for the pie chart
#         plt.title("Distribution of Categories")

#         plt.show()

#     def __calcSum(self, transaction_list):
#         calc_sum = 0
#         for t in transaction_list:
#             calc_sum += t.value

#         return calc_sum
