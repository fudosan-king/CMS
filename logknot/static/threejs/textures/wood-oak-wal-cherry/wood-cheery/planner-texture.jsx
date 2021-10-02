import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'wood_cheery': {
                name : translator.t('Cheery'),
                uri: require('./7.jpg'),
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#F6D8CE'
            }   
        };
    },
};