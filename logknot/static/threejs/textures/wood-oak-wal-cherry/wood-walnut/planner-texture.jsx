import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'wood_walnut': {
                name : translator.t('Walnut'),
                uri: require('./go-wanut.jpg'),
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#371D01'
            }   
        };
    },
};