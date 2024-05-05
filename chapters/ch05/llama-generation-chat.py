import stabilityai

def generate_image(prompt):
   # Create a new Stability AI client
   client = stabilityai.Client()

   # Set the prompt for the image generation
   client.set_prompt(prompt)

   # Generate the image
   image = client.generate_image()

   # Save the image to a file
   with open("image.jpg", "wb") as f:
       f.write(image)

   return image

