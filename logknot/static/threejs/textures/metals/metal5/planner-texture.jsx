import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'metal_5': {
                name : translator.t('Metal') + " 5",
                uri: require('./color.jpg'),
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#532F1C'
            }   
        };
    },
};