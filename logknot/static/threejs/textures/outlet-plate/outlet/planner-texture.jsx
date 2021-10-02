import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'outlet': {
                name : translator.t('Outlet plate'),
                uri: require('./outlet.jpg'),
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#fbfafa'
            }   
        };
    },
};