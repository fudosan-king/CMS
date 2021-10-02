import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'rusty_greige': {
                name : translator.t('Rusty greige'),
                uri: require('./rusty.jpg'),
                base64: '',
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#C8BFB6'
            }   
        };
    },
};