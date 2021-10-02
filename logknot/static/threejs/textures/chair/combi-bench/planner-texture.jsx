import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'combi_bench': {
                name : translator.t('Cushion'),
                uri: require('./combi.jpg'),
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#424242'
            }   
        };
    },
};