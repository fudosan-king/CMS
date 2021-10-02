import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'color_wood_oak1': {
                name : translator.t('Wood oak 2'),
                uri: require('./wood2.jpg'),
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#7C4917'
            }   
        };
    },
};