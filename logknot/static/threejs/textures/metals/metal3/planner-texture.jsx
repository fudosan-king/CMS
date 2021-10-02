import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'metal_3': {
                name : translator.t('Metal') + ' 3',
                uri: require('./metal3.jpg'),
                lengthRepeatScale: 0.001,
                heightRepeatScale: 0.001,
                mesh : mesh,
                color: '#AFAEAD'
            }   
        };
    },
};