import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'tap_1': {
                name : translator.t('Tap') + '1',
                uri: require('./metal_2.jpg'),
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#984e28'
            }   
        };
    },
};