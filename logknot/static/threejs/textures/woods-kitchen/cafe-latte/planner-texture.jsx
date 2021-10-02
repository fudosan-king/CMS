import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'cafe_latte': {
                name : translator.t('Cafe Latte'),
                uri: require('./cafe-latte.jpg'),
                base64: '',
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#F8F5F0'
            }   
        };
    },
};