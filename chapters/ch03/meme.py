import matplotlib.pyplot as plt
from PIL import Image
from matplotlib import rcParams


# Create the meme
fig, ax = plt.subplots(1, 3, figsize=(15, 5))
font_size = 12

# Panel 1
ax[0].set_facecolor('black')
ax[0].set_xticks([])
ax[0].set_yticks([])
ax[0].set_title("Human: Solve this complex problem for me", 
                color=black, fontsize=font_size)

# Panel 2
ax[1].set_facecolor('black')
ax[1].set_xticks([])
ax[1].set_yticks([])
ax[1].set_title("AI: Done!", color=text_color, fontsize=font_size)

# Panel 3
ax[2].set_facecolor('black')
ax[2].set_xticks([])
ax[2].set_yticks([])
ax[2].set_title('Human: Now, can you understand sarcasm?', 
                color=text_color, fontsize=font_size)
ax[2].text(0.5, 0.5, "AI: Working on it...", color=text_color, fontsize=font_size, 
           ha='center', va='center')

plt.tight_layout()
plt.savefig("/mnt/data/AI_meme_v2.png")
plt.show()
