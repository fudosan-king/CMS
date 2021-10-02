import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'outlet_white': {
                name : translator.t('Outlet white'),
                uri: require('./white.jpg'),
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#FFFFFF'
            }   
        };
    },
};