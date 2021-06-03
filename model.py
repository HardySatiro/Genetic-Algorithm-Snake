import tensorflow as tf

class Model():
    def __init__(self, n_input, n_hidden_1, n_hidden_2, n_hidden_3, n_classes):
        glorot_init = tf.initializers.glorot_uniform()

        self.w1 = tf.Variable(glorot_init([n_input, n_hidden_1]))
        self.w2 = tf.Variable(glorot_init([n_hidden_1, n_hidden_2]))
        self.w3 = tf.Variable(glorot_init([n_hidden_2, n_hidden_3]))
        self.wout = tf.Variable(glorot_init([n_hidden_3, n_classes]))

        self.b1 = tf.Variable(glorot_init([n_hidden_1])),
        self.b2 = tf.Variable(glorot_init([n_hidden_2])),
        self.b3 = tf.Variable(glorot_init([n_hidden_3])),
        self.bout = tf.Variable(glorot_init([n_classes]))

    def predict(self, x):
        x = tf.constant(x, dtype=tf.float32)

        layer_1 = tf.keras.activations.relu(tf.tensordot(x, self.w1, axes=1) + self.b1).numpy()
        layer_2 = tf.keras.activations.relu(tf.tensordot(layer_1, self.w2, axes=1) + self.b2).numpy()
        layer_3 = tf.keras.activations.relu(tf.tensordot(layer_2, self.w3, axes=1) + self.b3).numpy()
        output = tf.keras.activations.softmax(tf.tensordot(layer_3, self.wout, axes=1) + self.bout).numpy()

        return output

    def get_weights(self):
        try:
            weigths = [self.w1.numpy(), self.b1.numpy(), self.w2.numpy(), self.b2.numpy(), self.w3.numpy(),
                       self.b3.numpy(), self.wout.numpy(), self.bout.numpy()]
            return weigths
        except:
            weigths = [self.w1.numpy(), self.b1[0].numpy(), self.w2.numpy(), self.b2[0].numpy(), self.w3.numpy(),
                       self.b3[0].numpy(), self.wout.numpy(), self.bout.numpy()]
            return weigths

    def set_weights(self, ind):

        self.w1 = tf.Variable(ind[0], dtype="float32")
        self.w2 = tf.Variable(ind[2], dtype="float32")
        self.w3 = tf.Variable(ind[4], dtype="float32")
        self.wout = tf.Variable(ind[6], dtype="float32")

        self.b1 = tf.Variable(ind[1], dtype="float32")
        self.b2 = tf.Variable(ind[3], dtype="float32")
        self.b3 = tf.Variable(ind[5], dtype="float32")
        self.bout = tf.Variable(ind[7], dtype="float32")