import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'color_stone': {
                name : translator.t('Black'),
                uri: require('./black-stone.jpg'),
                lengthRepeatScale: 3,
                heightRepeatScale: 3,
                mesh : mesh,
                color: '#000000'
            }   
        };
    },
};