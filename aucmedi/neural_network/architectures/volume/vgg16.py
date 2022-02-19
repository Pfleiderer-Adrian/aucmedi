#==============================================================================#
#  Author:       Dominik Müller                                                #
#  Copyright:    2022 IT-Infrastructure for Translational Medical Research,    #
#                University of Augsburg                                        #
#                                                                              #
#  This program is free software: you can redistribute it and/or modify        #
#  it under the terms of the GNU General Public License as published by        #
#  the Free Software Foundation, either version 3 of the License, or           #
#  (at your option) any later version.                                         #
#                                                                              #
#  This program is distributed in the hope that it will be useful,             #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of              #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
#  GNU General Public License for more details.                                #
#                                                                              #
#  You should have received a copy of the GNU General Public License           #
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.       #
#==============================================================================#
#-----------------------------------------------------#
#              REFERENCE IMPLEMENTATION:              #
# https://github.com/ZFTurbo/classification_models_3D #
#   Solovyev, Roman & Kalinin, Alexandr & Gabruseva,  #
#                  Tatiana. (2021).                   #
#    3D Convolutional Neural Networks for Stalled     #
#              Brain Capillary Detection.             #
#-----------------------------------------------------#
#                  REFERENCE PAPER:                   #
#                    04 Sep 2014.                     #
#   Very Deep Convolutional Networks for Large-Scale  #
#                  Image Recognition.                 #
#          Karen Simonyan, Andrew Zisserman.          #
#           https://arxiv.org/abs/1409.1556           #
#-----------------------------------------------------#
#                   Library imports                   #
#-----------------------------------------------------#
# External libraries
from tensorflow.keras.models import Model
from tensorflow.keras import layers
from classification_models_3D.tfkeras import Classifiers
# Internal libraries
from aucmedi.neural_network.architectures import Architecture_Base

#-----------------------------------------------------#
#              Architecture class: VGG16              #
#-----------------------------------------------------#
""" The classification variant of the VGG16 architecture.

Methods:
    __init__                Object creation function
    create_model:           Creating the VGG16 model for classification
"""
class Architecture_VGG16(Architecture_Base):
    #---------------------------------------------#
    #                Initialization               #
    #---------------------------------------------#
    def __init__(self, channels, input_shape=(64, 64, 64)):
        self.input = input_shape + (channels,)

    #---------------------------------------------#
    #                Create Model                 #
    #---------------------------------------------#
    def create_model(self, n_labels, fcl_dropout=True, out_activation="softmax",
                     pretrained_weights=False):
        # Get pretrained image weights from imagenet if desired
        if pretrained_weights : model_weights = "imagenet"
        else : model_weights = None

        # Obtain VGG16 as base model
        VGG16, preprocess_input = Classifiers.get("vgg16")
        base_model = VGG16(include_top=False, weights=model_weights,
                           input_tensor=None, input_shape=self.input,
                           pooling=None)
        top_model = base_model.output

        # Add classification head as top model
        top_model = layers.GlobalAveragePooling3D(name="avg_pool")(top_model)
        if fcl_dropout:
            top_model = layers.Dense(units=512)(top_model)
            top_model = layers.Dropout(0.3)(top_model)
        top_model = layers.Dense(n_labels, name="preds")(top_model)
        top_model = layers.Activation(out_activation, name="probs")(top_model)

        # Create model
        model = Model(inputs=base_model.input, outputs=top_model)

        # Return created model
        return model
