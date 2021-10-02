import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'bathtub_1': {
                name : translator.t('Yellow'),
                uri: require('./bathtub2.jpg'),
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#EEDFB3'
            }   
        };
    },
};