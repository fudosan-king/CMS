import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'outlet_black': {
                name : translator.t('Outlet black'),
                uri: require('./black.jpg'),
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#000000'
            }   
        };
    },
};