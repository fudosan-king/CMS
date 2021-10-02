import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'metal_6': {
                name : translator.t('Metal')+ " 6",
                uri: require('./color2.jpg'),
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#837B77'
            }   
        };
    },
};