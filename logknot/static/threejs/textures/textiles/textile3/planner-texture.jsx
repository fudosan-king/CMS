import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'textile_3': {
                name : translator.t('Textile 3'),
                uri: require('./textile3.jpg'),
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#bfb45b'
            }   
        };
    },
};