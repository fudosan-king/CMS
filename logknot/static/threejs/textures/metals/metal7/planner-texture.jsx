import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'metal_7': {
                name : translator.t('Metal') + " 7",
                uri: require('./sliver.jpg'),
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#837B77'
            }   
        };
    },
};