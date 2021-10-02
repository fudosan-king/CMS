import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'kit_1': {
                name : translator.t('Kitchen') + '1',
                uri: require('./kit-1.jpg'),
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#F7F2EF'
            }   
        };
    },
};