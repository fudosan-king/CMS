import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'textile_default': {
                name : translator.t('Default'),
                uri: require('./textile_default.jpg'),
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#436b7e'
            }   
        };
    },
};