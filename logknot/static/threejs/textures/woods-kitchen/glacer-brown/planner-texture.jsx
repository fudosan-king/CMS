import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'glacer_brown': {
                name : translator.t('Glacer brown'),
                uri: require('./glacer-brown.jpg'),
                base64: '',
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#AD9980'
            }
        };
    },
};