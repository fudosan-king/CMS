import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'metal_4': {
                name : translator.t('Metal') + ' 4',
                uri: require('./metal4.jpg'),
                lengthRepeatScale: 0.001,
                heightRepeatScale: 0.001,
                mesh : mesh,
                color: '#6C6B6B'
            }   
        };
    },
};