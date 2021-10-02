import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'stone_black': {
                name : translator.t('Black'),
                uri: require('./black.jpg'),
                lengthRepeatScale: 0.1,
                heightRepeatScale: 0.1,
                mesh : mesh,
                color: '#000000'
            }   
        };
    },
};