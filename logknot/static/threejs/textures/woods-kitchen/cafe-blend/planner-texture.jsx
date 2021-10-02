import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'cafe_blend': {
                name : translator.t('Cafe Blend'),
                uri: require('./cafe-blend.jpg'),
                base64: '',
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#9B6E45'
            }   
        };
    },
};