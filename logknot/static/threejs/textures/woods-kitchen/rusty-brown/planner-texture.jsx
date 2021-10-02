import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'rusty_brown': {
                name : translator.t('Rusty brown'),
                uri: require('./rusty-brown.jpg'),
                base64: '',
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#4A362F'
            }   
        };
    },
};