import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'rusty_charcoal': {
                name : translator.t('Rusty charcoal'),
                uri: require('./rusty-charcoal.jpg'),
                base64: '',
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#585448'
            }   
        };
    },
};