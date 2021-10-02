import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'metal_2': {
                name : translator.t('Metal') + ' 2',
                uri: require('./metal2.jpg'),
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#DCEAEA'
            }   
        };
    },
};