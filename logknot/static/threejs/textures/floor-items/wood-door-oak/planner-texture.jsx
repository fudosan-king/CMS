import Translator from '../../../../../../src/translator/translator';
let translator = new Translator();
export default {
    textureProperties: function (mesh) {
        return { 
            'wood_door_oak': {
                name : translator.t('Wood Door Oak'),
                uri: require('./go-oak.jpg'),
                lengthRepeatScale: 1,
                heightRepeatScale: 0.6,
                mesh : mesh,
                color: '#FAE249',
                hidden: true,
            }   
        };
    },
};