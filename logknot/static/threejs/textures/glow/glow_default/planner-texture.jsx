import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'glow_default': {
                name : translator.t('Default'),
                uri: require('./glow.jpg'),
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#FFFFFF'
            }   
        };
    },
};