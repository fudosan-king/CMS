import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'wood_kitchen_oak': {
                name : translator.t('Wood Kitchen Oak'),
                uri: require('./go-oak1.jpg'),
                lengthRepeatScale: 1,
                heightRepeatScale: 1,
                mesh : mesh,
                color: '#FFED7B',
                hidden: true,
            }   
        };
    },
};