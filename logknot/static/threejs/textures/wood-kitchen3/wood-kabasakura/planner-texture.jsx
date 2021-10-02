import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'wood_kabasakura': {
                name : translator.t('Kabasakura'),
                uri: require('./kabasakura.jpg'),
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#7F5111'
            }   
        };
    },
};