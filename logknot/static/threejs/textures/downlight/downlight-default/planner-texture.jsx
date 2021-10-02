import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'downlight_default': {
                name : translator.t('Default'),
                uri: require('./texture.jpg'),
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#F2F2F2'
            }   
        };
    },
};