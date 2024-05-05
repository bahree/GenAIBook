import matplotlib.pyplot as plt

# Original probabilities
tokens = ['apple', 'banana', 'cherry']
probabilities = [0.3, 0.5, 0.2]

# Adjusted probabilities with logit bias
adjusted_probabilities = [0.5, 0.2, 0.3]

# Setting up the bar chart
barWidth = 0.3
r1 = range(len(probabilities))
r2 = [x + barWidth for x in r1]

plt.bar(r1, probabilities, width=barWidth, color=(10/255, 137/255, 2/255), align='center', label='Original Probabilities')
plt.bar(r2, adjusted_probabilities, width=barWidth, color=(128/255, 194/255, 29/255), align='center', label='Adjusted with Logit Bias')

# Labeling the chart
plt.xlabel('Tokens', fontweight='bold')
plt.xticks([r + barWidth for r in range(len(probabilities))], tokens)
plt.ylabel('Probability')
plt.title('Effect of Logit Bias on Token Probabilities')
plt.legend()

# Show the chart
plt.tight_layout()
plt.show()
