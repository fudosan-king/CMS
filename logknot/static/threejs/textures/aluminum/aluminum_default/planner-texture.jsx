import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'aluminum_default': {
                name : translator.t('Default'),
                uri: require('./aluminum.jpg'),
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#0B4C5F'
            }   
        };
    },
};