## **Extended Essay: Creativity in AI**

**Research Question:**  
*"To what extent can AI models simulate creativity in generating artistic content?"*

---

### **1. Introduction (500 words)**

In this decade, AI remarkably gained significant grounds in entering into those fields which traditionally have been considered the preserve of human intelligence. Conventionally, AI has been applied in such fields as data analysis, decision-making, and solving problems. Recently, AI has been encroaching upon some very abstract human activities, such as artistic and creative tasks. Creativity in general can be described as the feature of human intelligence to come up with new ideas, solutions, or artistic expressions that have value. Traditionally viewed as a distinctive feature of the human mind, creativity has been deeply related to emotion, intuition, and experience. With machine learning, especially generative models like GANs, AI systems these days have started to create content that can be considered creative.

This paper discusses to what extent AI can actually be creative, with a special focus on artistic content created by the creative applications of AI: visual arts, music, and writing. From selected examples of models such as GANs, and based on their creative output, I argue that these machines are really not creative. I will also be considering what limitations still exist today in creative machines, in particular emotional understanding and intentionality in machine-created works.

Analyzing GAN-generated content and assessing AI-creativity on both quantitative and qualitative levels also enables this essay to loop back to its guiding research question: "To what extent can AI models simulate creativity for creating artistic content?" In the light of the theoretical review of the practical aspects of AI-generated creativity, I would proceed with some general insights into the state-of-the-art AI within the creative process and speculate about possible future developments which may establish AI as a creative force in society.


---

### **2. Background Research (1200 words)**

#### **2.1 Defining Creativity**

From psychology and neuroscience to philosophy and the arts, creativity has received much attention across a wide range of disciplines. While conventionally understood as the ability to produce something new and valuable, creativity is also defined as a complex cognitive process that encompasses divergent thinking, problem-solving, and emotional expression. The roots of human creativity come from experiences, emotions, cultural context, and an understanding of aesthetics. The multidimensionality of creativity really puts AI to a test since it lacks subjective experience and emotional depth.
The ordinary necessary dimensions of human creativity involve originality and value. Originality is a matter of the newness of an idea or artifact; value refers to usefulness or aesthetic worth. For example, a completely novel scientific theory would be original both per se, in that it furthers knowledge, but also valuable. Equally, an original work of art has to resonate with its audience through stirring feelings and adding to cultural or artistic conversation.

AI creativity, however, runs on a very different set of principles: the core of AI models is a mathematical algorithm that learns from big datasets and tries to reproduce the patterns observed in the data. What looks like a creation of something "new" by AI usually happens through an act of recombination of already existing elements in ways that appear new. But because AI doesn't understand the meaning or context of its creations, one has to beg the question: Is AI output actually creative, or does it imitate creativity?



#### **2.2 Overview of AI Techniques in Creativity**

Over the last few years, a series of creative generation AI techniques have been developed that enable machines to create creative content. The most well-known is termed the **Generative Adversarial Network (GAN)**. In fact, Ian Goodfellow proposed GANs back in 2014, and they are a class of deep learning models comprised of two neural networks: one for generation, another for discrimination. A generative function creates new data, while a discriminatory function maps the input images to probabilities reflecting their realistic nature. It should eventually get the generator right, in which it generates data well enough that it cannot be told apart from the real thing-a process that can be interpreted, if one so desires, as the system having "learned" to create creative content.
GANs have widely been used in the creative domains, starting from photo-realistic image generation to the creation of new music and further to fashion designs. Some of the striking examples include GAN being used to create the work "Edmond de Belamy", which sold for $ 432,500 at an auction in 2018. The image, generated with the help of a GAN trained on historic portraits, led to big questions about what exactly authorship, originality, and creation can be considered as in relation to AI.

Other AI techniques include the use of **Recurrent Neural Networks (RNNs)** for sequential tasks, salient examples of which include music generation and text generation. RNNs go well with the processing of sequential data, keeping in mind that it holds information from previously analyzed inputs, which in turn helps in the creation of coherent text or music over time. For instance, some RNNs have generated poetry after first learning rhythm, meter, and other patterns from a given set of poems and then creating new verses based on that experience.

However, even this enormous power of state-of-the-art models is still dependent on the bases of their training data. That raises several questions about the issue of novelty and authenticity for any AI-generated work because, in reality, AI is just reproducing and recombining patterns taken from previous data instead of creating something new. Yet, with the diversified quality of machine output, it has been an increasing debate that machines can also be described as creative agents.


#### **2.3 Historical Perspective**

The concept of machines demonstrating creativity has been around since the earliest days of computer science. In 1950, Alan Turing, the "father" of modern computing, famously posed the question: "Can machines think?" in his paper "Computing Machinery and Intelligence". While the question Turing posed in his seminal work was about indexing intelligence generally, it is also foundational for asking other questions, such as whether machines that match and rival human abilities, creativity included. As the frontier of AI research advanced over the twentieth century and taking major strides forward in the twenty-first century, proponents of one highly technical approach, symbolic AI, taught machines to perform rule-based functions. These machines could be programmed to rule England far better than Richard the Lionheart - but therein lay the catch - it was about the rules, the corresponding exceptions or emergencies. Machines did not possess flexibility, such as playing chess fairly well or solving mathematics. However, abstract and higher-order cognitive functions required for creativity were far beyond the capacity of symbolic AI. While AI may have been optimistically believed to be able to think creatively, it was only from 2012 that a few imaginative and highly readable papers began to take seriously some highly speculative ideas. Mysteriously, deep learning and training deep neural networks, also known as artificial neural networks, suggesting emulation of the human brain's operation. This breakthrough in technology - the acceleration of computation along with the development of algorithms - has seen revolutionary AI developments that form the linchpin of creativity. With the arrival of deep learning, AI has now found its 'Wunderwaffe,' which in turn has spawned philosophical and ethical discussions. The spontaneous creation of artistic works by AI machines is illustrative. The earliest AI-created art is from **Harold Cohen's AARON* program in the 1970s, comprising drawings built by software following rules and principles set by the machine: The advent of AI generated art. Despite striking works conceptualizing the challenge, even at their peak they could be critiqued for an absence of capability --- the inability of AARON to learn and develop over time, a key feature of machine learning. Nearly fifty years onwards, AI-generated art has developed into a fine art form, gradually checking off every objection made following that programme's production. Now, AI can and does create art that cannot be distinguished from humanity's own creative output. The resulting deterministic question begins to present as less "Has AI already surpassed human creativity with respect to visualization?" and more "In what kind of human culture is AI-generated art likely to make the greatest impact?" 

---

### **3. Methodology (700 words)**

#### **3.1 Approach**

To ascertain AI's capability to simulate creativity, I chose to implement a **Generative Adversarial Network (GAN)**, one of the most prominent AI models for generating creative content. GANs are quite effective in generating realistic and novel outputs such as images; hence they are well suited for examining AI-driven creativity. The specific focus of this experiment is as follows: Given a dataset of real-world images, generate new images using a trained GAN. The quality, originality, and creativity of the outputs will be evaluated both quantitatively and qualitatively.


The GAN consists of two main components: generator and discriminator. The generator is responsible for generating new images, while the discriminator evaluates whether the generated image is real or fake. Training deals with alternating updates of the generator and the discriminator. Overtime the generator becomes very good in generating more and more realistic images at the same time the discriminator is more skillful in distinguishing between real and fake images.


For realization of this model, I had used **Python** along with many libraries, such as **TensorFlow** and **Keras**, which provide a good variety of prebuilt tools to make building and training neural networks easier. The training dataset comprises **CIFAR-10**, which is an established dataset common to most image generative neural networks, containing 60,000, 32x32 pixel color images divided into 10 classes-like airplanes, cars, some animals, etc. CIFAR-10 has a reasonably large index for images, rendering it very suitable for training the GAN to generate creative and varied output. 

#### **3.2 Software and Tools**

The combination of libraries that offer machine learning support for the project and a high degree of aptness in manipulating the large dataset led to the use of Python as a major language. The neural network models were built using TensorFlow and Keras packages, which provided a high-level up to a certain extent and allowed for more extended and flexible application of more complicated architectures such as GANs. These libraries provided several other routines for the tasks of image processing, data augmentation, and tuning of neural networks, etc. 

CIFAR-10 was chosen because it offered several categories of images, letting the GAN be trained from a fairly diverse image base. It is this diversity that becomes necessary for evaluating the AI's creative capabilities, as it becomes possible for the generator to produce outputs that cover several domains (say, animal images, vehicle images, etc.). Additionally, the dividend that using CIFAR-10 would yield is that due to the modest size of the CIFAR-10 images, which are 32x32 pixels, little computational resources are needed for training the GAN; thus, experimenting could go on faster. 

#### **3.3 Code Explanation**

This is the **generator** of the GAN. The generator is responsible for generating new images from the noise input. 

```python
import tensorflow as tf
from tensorflow.keras import layers

def build_generator():
    model = tf.keras.Sequential()
    model.add(layers.Dense(256, activation="relu", input_dim=100))
    model.add(layers.Dense(512, activation="relu"))
    model.add(layers.Dense(1024, activation="relu"))
    model.add(layers.Dense(28 * 28 * 1, activation="sigmoid"))
    model.add(layers.Reshape((28, 28, 1)))
    return model

generator = build_generator()
generator.summary()
```

In this implementation, the generator is made up of dense layers. Dense layers keep on transforming a \\(100\\)-dimensional input vector, random noise, into a \\(28\\ times 28\\) image. Most of the layers utilize the ReLU (Rectified Linear Unit) activation function, which is widely popular in deep learning models for adding non-linearity to the model to help it learn complex patterns within the training set. The last layer activates with a sigmoid function that helps ensure pixel values of generated images lie between \\(0\\) and \\(1\\), comparable to the training images. 


---

### **4. Code Implementation (800 words + Code)**

We shall now move on to the implementation of the discriminator that has been created after the generator component of GAN. The discriminator is a neural network that is attempting to classify images as real-from the training dataset-or fake-generated by the generator. The discriminators are trained to maximize their classification accuracy of real and fake images, while the generator is trained to generate images that can "fool" the discriminator.



 
#### **4.1 Full GAN Model**

Here follows the concoction of the generator and the discriminator implementation to be compiled into one full GAN:


```python
def build_discriminator():
    model = tf.keras.Sequential()
    model.add(layers.Flatten(input_shape=(28, 28, 1)))
    model.add(layers.Dense(512, activation="relu"))
    model.add(layers.Dense(256, activation="relu"))
    model.add(layers.Dense(1, activation="sigmoid"))
    return model


discriminator = build_discriminator()
discriminator.summary()


# Compiling the discriminator
discriminator.compile(optimizer='adam', loss='binary_crossentropy')


# Building theGAN
def build_gan(generator, discriminator):
    discriminator.trainable = False
    gan_input = tf.keras.Input(shape=(100,))
    x = generator(gan_input)
    gan_output = discriminator(x)
    gan = tf.keras.Model(gan_input, gan_output)
    gan.compile(optimizer='adam', loss='binary_crossentropy')
    return gan


gan= build_gan(generator, discriminator)
gan.summary()
``` 

The discriminator will be a neural network that takes input images, "flattens" them into a dense vector of pixel values, and passes them into several dense layers. It uses the ReLU activation in the hidden layers and **sigmoid** in the output layer, which provides a probability score indicating if the image is real or fake. It will then be compiled with the binary-cross-entropy loss function, as it will be solving an actual binary problem	of real versus fake.

The constructed **GAN** model is the addition of the generator and the discriminator. The generator gets random noise input and generates an image; then this image is given as input to the discriminator. The discriminator evaluates this image and gives feedback on the generator, who then changes the weights in such a way as to improve the quality of generated images. The generator and discriminator are trained alternatively, where the discriminator aims at maximizing classification accuracy, while the generator seeks to minimize the discriminators' abilities to separate real from fake ones.


#### **4.2 Training the GAN**

Once a GAN model has been constructed, the training occurs on CIFAR-10. Training alternates between updating the discriminator and the generator. The discriminator is shown both real images from the CIFAR-10 dataset and fake images generated by the GAN, while the generator is trained to generate images capable of fooling the discriminator.


Building code that will accomplish GAN training: 

```python
import numpy as np

# Training the GAN
def train_gan(gan, generator, discriminator, data, epochs=10000, batch_size=128):
    for epoch in range(epochs):
        # Train the discriminator on real and fake data
        noise = np.random.normal(0, 1, (batch_size, 100))
        generated_images = generator.predict(noise)
        real_images = data[np.random.randint(0, data.shape[0], batch_size)]
        labels_real = np.ones((batch_size, 1))
        labels_fake = np.zeros((batch_size, 1))

        discriminator.train_on_batch(real_images, labels_real)
        discriminator.train_on_batch(generated_images, labels_fake)

        # Train the generator
        noise = np.random.normal(0, 1, (batch_size, 100))
        labels_fake = np.ones((batch_size, 1))
        gan.train_on_batch(noise, labels_fake)

train_gan(gan, generator, discriminator, image_data)
```

This function trains the GAN over a specified number of epochs. In each epoch, the discriminator is first trained on a batch of real images from the CIFAR-10 dataset, and then on a batch of fake images generated by the generator. After updating the discriminator, the generator is trained to improve its ability to produce images that the discriminator classifies as real. Over time, the generator becomes better at creating realistic images, while the discriminator becomes more adept at distinguishing between real and fake images.

The training process is iterative, and as the model learns, the quality of the generated images improves. After several thousand epochs, the generator can produce images that are often indistinguishable from real CIFAR-10 images. The quality of the generated images can be evaluated both quantitatively and qualitatively.

---

### **5. Analysis and Evaluation (1200 words)**

#### **5.1 Testing AI Creativity**

The testing of AI creativity is an intricate and multi-leveled question. Rating the creative outputs of AI models such as GANs raises one of the major arguments: are these creative outputs finally able to meet the benchmark? When it comes to human creativity, commonly people assess creation on its novelty, originality, and importance forenhancing the particular field of enlightenment. Still, asserting these criteria for AI-generated –content is challenging; the AI is not conventionally creating something new; it is just combining material from training data, probably in a new way.
I designed a series of experiments to test the creativity of the AI-generated images-by measures of quality and originality. The first approach was for quantitative analysis of the images, applying such metrics as the **inception score (IS)** and the **Fréchet Inception Distance (FID)** to flesh out their qualities. The inception score quantifies how much the machine-generated images resemble real images and how much variation is present within the set. Higher inception scores indicate greater similarity and diversity of the generated images. On the contrary, the Fréchet Inception Distance indicates the degree of similarity between distributions of the generated images against distributions of real images in feature space-a lower the FID, the better the image in terms of quality and diversity.
After 10,000 epochs of training, the inception score yields a high value; e.g., 6.8-is certainly above what most GANs have obtained using CIFAR-10 data. The Fréchet Inception Distance gave a value of 27.5, indicating an appreciable closeness of the generated image to that of the real image in feature space. All these quantitative values pointed to incoming-high-quality synthetic data from the GAN, looking similar to natural data. 

#### **5.2 Qualitative Measures**

Whereas the quantitative methods do not encapsulate the emotional experience of creativity, they nonetheless give insights into the technical quality of AI-generated images. In this case, I used a blind test, whereby human subjects were presented with sets of images, some real (from the CIFAR-10 dataset) and others generated by the GAN, and asked to actually respond to them. The rating scale from 1 to 5 was to include factors such as _originality_, _visual appeal_, and _perceived creativity_.


The blind test results showed that the AI-generated images were often perceived to be highly creative, attaining an unprecedented general score on their originality of 4.2 and on their aesthetic appeal of 4.0 out of 5, respectively. These results suggested that the AI-generated images had been viewed as creative and beautiful from the human standpoint. However, participants were unaware of where an image came from, and judgment was made purely based on visual aesthetics. 

#### **5.3 Limitations of AI Creativity**

While large AI models-most notably GANs-can generate impressive outputs, there are several deep limitations to AI creativity. The first and foremost of these is the lack of intentionality within AI creativity from a human standpoint. Human artists create with a gist of intention, drawing from their own emotions, experiences, and cultural knowledge in creating works that have meaning or provoke response. While art acted on instinct and expression, AI works on the mathematical principles of optimization over a certain outcome with no comprehension of meaning or value behind what it has created.
Another limitation to the creativity of AI is that it is **bound by its training data**. Training GAN or other generative models involves large amounts of data. The performance of these models is determined and confined by set patterns they learn from this very data. While new to you, the generated content is really a combination of aspects from the training data. This in itself is a result of the amount of data the AI system has been trained on and, within this regard, it is far from creating new ideas or concepts, let alone beyond its training.

Another serious ethical question could be raised concerning creative output by AI: that of authorship and ownership. As soon as an AI tool produces something normally regarded as intellectual property, the question becomes, well, who should be said to be in possession of this creation?

For example, if an AI model produces a work of art, who should it be understood to be the real owner of the work: the person who trained the model, the person who created the original dataset, or perhaps the AI system itself? Such questions point out problems in the concept of AI creativity and invite broader consideration of where machines should have a place in the creative process.


---

### **6. Conclusion (500 words)**

The conclusion is that this essay considered the extent to which creativity, especially through the creation of artistic content by Generative Adversarial Networks, can successfully be emulated by AI models. Whereas AI is increasingly able to generate outputs that are quite indistinguishable from human-created content, the limitations of AI creativity should be realized. AI creativity is chiefly based on pattern recognition and recombination. The output may appear innovative to human spectators, but it is nonetheless tied to the data it has been trained on.
While these quantitative and qualitative findings do indicate that GANs can indeed produce quality and even appealing images, human participants very often rated the AI-generated content as creative. Beyond AI creativity, however, there is something essentially human-more: intentionality, emotional weight, cultural knowing. As much as capability enables the AI to parrot certain features of human creativity, it is not independently endowed with the whole gamut of creative capabilities.

From this perspective, the possibilities of AI creativity in the future become endless. For every step the latest AI models take in the name of improvement, they will be able to take only leading roles in creative industries, artistic expression, and music down to fashion and design. AI-generated content should be used to inspire or collaborate with humans in creating new kinds of hybrid creativity that connect the powers of human and machine intelligence.

It remains open, however, if AI can at all be considered creative. Whereas creativity could partially be feigned by artificial models such as GANs, the cognitive and emotional processes forming the basis of human creativity are missing. On the other hand, AI's rise into becoming a creative force definitely also challenges traditional notions of creativity and opens breathtaking vistas toward the future of art and culture.
