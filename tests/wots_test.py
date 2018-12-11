#!/usr/bin/env python3

from specs.wots import *
from lib.speclib import *
from tests.testlib import print_dot, exit

# Generated with https://github.com/joostrijneveld/xmss-reference/
m1: digest_t = bytes.from_hex("b8cdb147973dea2ec70aa59ce71ec6d88277761d717221580eb847abd0a4e6a9")
seed1: seed_t = bytes.from_hex("c36ca7f20260dd3f0cc08133f7d86ee682579f61263b2e8d43b4b9630aa53028")
adr1: address_t = vlarray([uint32(0x7e7c37a3), uint32(0x0a43c868), uint32(0xfc72f92b), uint32(0x1644edcd),
                           uint32(0x8589250a), uint32(0x00000042), uint32(0x00000001), uint32(0x00000001)])
adr1p: address_t = vlarray([uint32(0x7e7c37a3), uint32(0x0a43c868), uint32(0xfc72f92b), uint32(0x1644edcd),
                            uint32(0x8589250a), uint32(0x00000042), uint32(0x0000000e), uint32(0x00000001)])
pk1: pk_t = vlarray([bytes.from_hex("156c09cec70795d96f1dff349f976bfc1bf9ae165eff96f47af28aed09335f7f"), bytes.from_hex("9c63b000f5e0a61faebd9219b7407e61d72c6ff53e550b4aff6be83822473e92"), bytes.from_hex("247d93a0c5a5f43f4c42d818af51f3ba80cb40afb35366b741775df934030005"), bytes.from_hex("fcb5315e681227eeb326eb3242df7496013d19ec5af27187b1c8b896c0cb97d2"), bytes.from_hex("0445d403d09f4293b8e0a15751cdbdb7cfd33885caf7a17ae81147bdb9f987c7"), bytes.from_hex("53ab5fb991656fccc6fba8024140f62d5d59251b78a35536b86e570ca4893736"), bytes.from_hex("18d6ec9309c32a0e37acdd60774ecb8b5cc07e69bbc8ec075697143472fb563c"), bytes.from_hex("5dedd5ef7fef2deb0e15c04e01404cdd729355721be62f995e78455144b7120a"), bytes.from_hex("4b37563dedf25fc01f40dae66d578959af08e1724912eb914f718ab7e11641f3"), bytes.from_hex("97799f82dfc77d993302234f3f241cf5e372a254dd84bae942fb6f4413d50735"), bytes.from_hex("5b639e1b9c4374f2da7d6a3c7034b7c1c4a0eac3f2157e4ce4fea9575a8275ce"), bytes.from_hex("958229b818581a1084c4462b17a47369405b5d5db56be1d53f1df8c1e69f2740"), bytes.from_hex("b15ce6028f38f4123b031fa2cf2643887bd8f743c96e34a932080c94f59981c1"), bytes.from_hex("021eddf56359d5d2089e066e4718a5a699e14e15686b1dbd2614ca07693af1fb"), bytes.from_hex("63dfe809cbe75c1fee78e979e6b00910180ad7e5c6ef9fe49d2f0dedc403c7d4"), bytes.from_hex("eb4c01b93ebf71cffb42c6cc2f81c2016d000b94cdd8c174a35a40c307fbfa5d"), bytes.from_hex("ac9fe7df3d2e2e48fa3a3b7973ae502eae4f50850e885bc653d8b985b818aa8d"), bytes.from_hex("b2d6c01cb82d132a59cdf5bee2b1e00752e38ace81a804a713cf5cfa11cbf892"), bytes.from_hex("7e1c8fab440db08e4525d9091db61ad56e63d2a1f5985e8535d04dfafe5f4b84"), bytes.from_hex("212eb9a212151e231cd3294037f025f510b20b403099e0f949033e78a9bb4ee4"), bytes.from_hex("45623bfa4d4e5246ad01c9118ba6f2129ee746e771aa706e3bcd9b3700832042"), bytes.from_hex("d7d6bb780408be8a1987295aab1e87ec61b15d8a0fbe89102b083fed78a8f4dc"), bytes.from_hex("d92d3c001d70fcf448e8095d9ae5b59b4ebc4de1d81cd7f9e49f74b5916e0eb2"), bytes.from_hex("2703da0174b7a1c63ec776b7761e55713b8ea8038fba5f12a0cb7be73701c825"), bytes.from_hex("d9c36c65a9b31666b1094b7711db2732cdb7286f28c72bc201fa40468889f991"), bytes.from_hex("4b1d86ae0e3206df92174fe06c7f90dabe1906f52314272ee53d327b8e5d02dc"), bytes.from_hex("39e3a8dd81f40034c49d2f4d208047ec6ecb6d7f1114fa814f54f365f26e350b"), bytes.from_hex("7aef634b169d6817c3ef7a322d9882fd67d2a5b69a2e8c6e5fb7bc269e092ea2"), bytes.from_hex("462df9ea9f49891fb22cd0be870335f1730f5d11bda6d9c2adc2d6a9be4db015"), bytes.from_hex("210e6f61e30d2ed986d7ced336ae1a06994110037186ce8a8a29235f91e080de"), bytes.from_hex("1434a617eea725302996b1bdaf63e68079315d98cd4f08b010d0c62903b3f023"), bytes.from_hex("7d5a86f3913e89c436de0a3312f4e6afcc40ca1aebc2c9b9be19d87faf3e94fb"), bytes.from_hex("293616b81027cf75838086792131d78ada949d47066e34a2e89e40450a135f5a"), bytes.from_hex("a3c9cb09f63ce7f5fea007784fe07bd9b130153c73fb189704872e65863d29a5"), bytes.from_hex("c975e749918650dee2446ae0c46b57ddaf90a616de7dd1d372096b5e885991a7"), bytes.from_hex("10d9f7c59b28977ea596333cfd1483c5a5ac8d70da35a19f0c04e6b6ad72ca32"), bytes.from_hex("5e439927bb3c8d837b9f45455e4621a8d3825d0135273dbc6a8a185d91b10ac5"), bytes.from_hex("6be8ac570333113cb15e5fdf830252d1dbf24d2380d7263246666dff0408f072"), bytes.from_hex("a6c798a4f19d5cdb13d8fe6fdfb6c3a8c8a6bb30e4f5fb74737a110fd36a5024"), bytes.from_hex("ce2bb5c5982522bc9d52a89f3eba10352f3fc79aa5bcabc2ce6f84b2f005665b"), bytes.from_hex("695ae07c708141c6d0e71c5c3ff0b6a2466fbc3b99eb277e436a7654ffb09fdc"), bytes.from_hex("51f098c9c54d5fce186723d8447773e6f7e8f0a871ebfdf005fcbd7e46bee0d5"), bytes.from_hex("e18e6a43952b21f13997711c8b5cd7b328a2b2b5cc106feb46e308214e0c7083"), bytes.from_hex("aec489e6b1374eedce74c3188297a7eff627466608b2498f36e92f087aaca8ea"), bytes.from_hex("1e814b04f037129d584e51a3306e20cd3b1941485c17f3a6ceec7ef56f901894"), bytes.from_hex("f3b59fb4620e4e1ab0bb13142e0d0ee18df56f5cd5f865597d6d42a01b82f58d"), bytes.from_hex("6849b7c12646126b62ab5e92677ea46dd381a2148d4abed5290c53a9ecf11d9f"), bytes.from_hex("1932b18d6ff132b4d37a91b9587da92eacc229a84650f8e15c876caa33c52f27"), bytes.from_hex("15c7159941e110ea8bda1297a33ca29ac43825d51a1cda11f654678461f8bff1"), bytes.from_hex("2d688ae625925af6e82de87f52ff15434475db2b72104bc4a70f4cc0a0e8f3ae"), bytes.from_hex("f7e70c9cb06e00aed29b763136edadfd5153100b42a433181c9df5287e7e05bc"), bytes.from_hex("8398a307993c049327aa743856c33afb06c6820ef5edbe5dfcee2161a7e549a0"), bytes.from_hex("2acdf74bd6eb0b960c0ff1971228b33abe58685e44a82600f99c10a5abe51da1"), bytes.from_hex("94c9bfe947e29f60fb7ea980db33241d8d631390c812477ffdb55b1a45974fbb"), bytes.from_hex("895c9234d3c22b6c758875b2f6531abd282107e403d19d5d206e4a542d737ef8"), bytes.from_hex("70bd408a73993c823b368a0a879363cba1b959db7237135fedda5f276cf19a68"), bytes.from_hex("ddead01689180611f6ff96808746173f4ca989ebfd238708d2e753b9dcf001a1"), bytes.from_hex("09d2ba5e290966bee8c4a3ed31da09c15c9473e1e91e1295a6ff436938bd9df2"), bytes.from_hex("ba7a53f4949bc98cf45967b46acfdbf1e89b8a1a18b2668345d45abb570a8168"), bytes.from_hex("24a6171b2830f685d561c4b31a3d0995d8cc8630e5c8f198c95cff64540604a5"), bytes.from_hex("3b4ad75b1c52eb26033f3a195255935f2280e8dd259006cb5bd9aae1f4bb8de2"), bytes.from_hex("ef91e29b73cea595daa70d33f32b2ebfae9ba5da8fbf9676d184bff6d8234109"), bytes.from_hex("7c6af998a67bc09c9c2f3cf2151d58156fe2c379ae30b096395e29745c409d76"), bytes.from_hex("718ff587af819ef90ef44fa111212a1b221e853e91861d7073c259db667cb1b8"), bytes.from_hex("f9d01dbf71a2119650c18c2626620ea4a1cb178a666f464bb7024464f7b4c34f"), bytes.from_hex("520c22176c61dc392e0b9f47c39b5e9c695613e3dda94e3bb1be7105fdeacdad"), bytes.from_hex("919ec89c5153601e669a92d0e62672e643113dd7cf5ff411ab2a880b73c077d1")])
sig1: sig_t = vlarray([bytes.from_hex("8b2d1ba56f629f9d35e85a18de3cbcf2152afa8cb3230fa009b1da466fb87976"), bytes.from_hex("0fc18b61c4f4b8fb369e933d1df4bb4f81628aa97e80fbef6fd84934e00e33e8"), bytes.from_hex("ab61e7926bcc9231c7a6d78b753ee0a337a9fef93ff9aa134ab87feefcdc0536"), bytes.from_hex("3ca08e9a428da3d66fabf1112b268d4ed100a0a95899a322ff68566579637c9a"), bytes.from_hex("ac357e7a8531a8cdec101f841d0eb1ec33ec826687fa1aaceb3838f99d99e8e2"), bytes.from_hex("a120494f2f4501557a9c0ceae3463f67d15b0287d01a715d24395ba60e7edd13"), bytes.from_hex("2b2e483dea637e790fb37a8b8a951c0060a892b75617f36d678393b4ac43f536"), bytes.from_hex("7be6cc03ae9a9c5f0a8063289598e101688ae8885ffa9e5bf79c62d03b9e91cb"), bytes.from_hex("dcd99338d98eac7fcc2dc2887a0b988c607996ef4254057e797b1e602bdb65dc"), bytes.from_hex("e4532770e2782742b0374d05a2afec6de8b83bd4df90de7c8e3c5e194224c250"), bytes.from_hex("41d9a0fc0a3909a2b801ac8a5172fe8167a2d52920f04ab5b1e01337e91215bc"), bytes.from_hex("80238ff9d7ca1e453abe6fe616a617f0f38921758b2c8fd446486379bcb0c0f9"), bytes.from_hex("33b8e321ba577cb9e39571844cf3c613f5411390cf675c0dee6878a3bc0e51b1"), bytes.from_hex("ab5e80c867b26dcabf0930843d89ae5e099a0801e9018e6da13360f9460a331e"), bytes.from_hex("5e1bb0cf4631200a92deccb0834810dd4b7cb735b7c85f69e0ba2a2f83ee0722"), bytes.from_hex("d80af9a7604d33f8ae44b8cbd33b8ad7170d09e27c43bf5a3462daa539b3b3f2"), bytes.from_hex("9ac69ba76abcf06afdcc604fc216cd7d1eb57b8c54ad4f0a250304ab69a000a5"), bytes.from_hex("19462ec163d9d2817f2020e55e0a364ac1b6875e2c38cee18ffda159ab9846fc"), bytes.from_hex("d171302d508161d8f950e3df69551ae1fe63eea54319755f061f33290c7cec07"), bytes.from_hex("9277fb4eb088d859aaa35fcb8719e8ca2d9e382deca462bf761c122bd6510b9c"), bytes.from_hex("9040689f685fe81436fe4098dde37b564ceabbe5ee83f46644a9d3881265b03a"), bytes.from_hex("57d63468da5cf2b45bdc4b0fac80d07de21b306a038404568ae2ba72a2e3aa59"), bytes.from_hex("64db0c4b3c883f4228139e208a6ac66234dfa6cd267282c5a73cba505c9bf049"), bytes.from_hex("0efbcecbd1ce456107db7b34da57a319f6b62fd5427f70ca16eb3dff7d0b0ea6"), bytes.from_hex("d70d88107bf780581e48f697f77a5a488dea59d1aa9e1e93ff7696f3f286e2c5"), bytes.from_hex("f7d23795f9f92619b1c2bc7afdf99723b3320df739d8631f3419f4182a5d42b8"), bytes.from_hex("2bde536c75c660e06dbe45b3979dc78899de7a06d7ca51db1b8211b99d6f5a48"), bytes.from_hex("cd924db3aa2b9130f6529b343c577e9ff2a152daae57588369d8793395c594f1"), bytes.from_hex("1b0ac8406fa32bc89ea8f6ad411043d235a28312a1272d9064a5f4fc2ef74270"), bytes.from_hex("af84b34a58e5a772905d4b603703e608016393bcf504e516a14e1a8438e38521"), bytes.from_hex("7c690bccf86aa60f0ec12ff98d9f33cf84aaa485dde50f95c0b8eca944675ed0"), bytes.from_hex("f60db4cfb9d96f2bc30748b8da3ed32186fc85c6de969e355c9f769c982c1df8"), bytes.from_hex("111fcd976a051a711ec787e1237b762f30d05c3eb0bc0cadd9079892655e3d59"), bytes.from_hex("2e6e1e46adff0d326631f28261685fa866da08b6a69884cdbc4d69ef3908cf72"), bytes.from_hex("af12994b8b949e6d49b9562938224dc38054b6c120196b201b800ad2de3f0d1a"), bytes.from_hex("9f0eb9a900f9d11791193987405d972880d42c4cce7929b787206544a020e3c4"), bytes.from_hex("331c05bab3c4cd0a574430f8494bdcaadfc6e09a25f9f3ddec919dc79c4fd3fb"), bytes.from_hex("3991201615cc7a8ee61fbed1ff1352da6d0f33ac492cd41ea862e24c2aef8458"), bytes.from_hex("1c09f5a72690044fba829dae248b4ee8a7e8eaddd70d6afe3503efaaf230dc88"), bytes.from_hex("1393f8d15434f519aae8971c09ed4652db481cbc9722356c84470900057d1c2d"), bytes.from_hex("4164ff60cef54b3efde23a3452a281ea7bb7710c9fd643c26af8bb63c938d854"), bytes.from_hex("0c041a1a3626d396c4f2635e996f115e203aeb36ef9ca98432fb469bc3d66881"), bytes.from_hex("6d518a067d823ffbeb9afbc468614d4d3c31dca6dc9e49846aae442b889ed6a9"), bytes.from_hex("83c76ecb1f2b51aeb66eaa43a924685862163ef32cb5796611d7662ddef02797"), bytes.from_hex("a0701425b6edb12f6e9032957610d19b7ac94fe4ddf4e3fd8e50d70abcb8bd15"), bytes.from_hex("545d929aa48fd262dc78af1b8da1b5d6d0180982c1ab83d0206cc447b6da310d"), bytes.from_hex("5b6871171c6ffbd3e09c6b14a75633775a8efe4599a1ef92020481ff7ceba583"), bytes.from_hex("820e20197cdf3b244c703e0eb4829392fa6e66a98db01a10cfb1d0aef9985a7d"), bytes.from_hex("7acc78611085b6c3e30f1c7891539ec8d33f63382067f1c5a9286031893b0a1c"), bytes.from_hex("ea0e8cfacc5ab3f301609f41d8a1b178c31de44d0953cc4592d40d4ae6a3174e"), bytes.from_hex("b7185545a6da539d380e24896f171aee1b244150db005912b0700f04eb719960"), bytes.from_hex("5967b2165be545f444d5b4fe71474b1bd176c6c58a6748038db73863f2b9bb62"), bytes.from_hex("5c6b73bcbd2985e7e477c29cd875717b81fa4c426e628e0af5fb475767c20457"), bytes.from_hex("e2fd2925d3497ebf3f3c63406e70f3252756bed9754b5f08de933cd98eb9bf7f"), bytes.from_hex("ed5816a5279b5f5545eb5a29bca497fbba7f7aba9f16aaa9892c8fe2c284ca5a"), bytes.from_hex("b3e2965bb51a4405ec85aeae7ef5a94d30972b30488d659efee297bcf48c63d3"), bytes.from_hex("edf326393e791cb58c8cd9230c0323d5f7c03db61f619266d5e55b7af25ee72d"), bytes.from_hex("d437b3bf35ffcf5c8f80b7a569a57e6cfaa2c895dc840e0590e74109d79e2b0b"), bytes.from_hex("a9dcf78d6c38d7f657d7ba0d7ac79663e2495e9e839fbc00759cefd5bca7909f"), bytes.from_hex("0b7e366f79cd02b6b2274936610307605eb0d807d8011f1207d048f87c6408a8"), bytes.from_hex("50f98fae5ae60c1e769649d9059a6b932dc401c4f387826b763bc408226932d2"), bytes.from_hex("329b85202762c8ddf1364a8d6f06028fd5a69d0cd98fcb6d8a32249562574b98"), bytes.from_hex("99a347fd50fbf9ff798d4a0b81d028e44119771b5c468680ae2005fc9e33baa6"), bytes.from_hex("be1646b3d45bce0d428ede87fb4d02d0c324eee64b97ff8029aa8a9e3c9827c8"), bytes.from_hex("67f61c1d28eba92a1ffcd7d666ac0f696ee1f37c085edb0a073bfa23a533eaef"), bytes.from_hex("04da3b5a97cbca9c51e21ef1cf41e1911e75b4e51420e3763c9168781c326333"), bytes.from_hex("38afda61ee2fac89cddb7439e286ade37a4241077e5ea817d9b8ec3d831ba518")])

m2: digest_t = bytes.from_hex("c469793f44fb35a484b6007ce01fe8c54b1dd9b2eced66e2bbdba849b5fb6ea5")
seed2: seed_t = bytes.from_hex("93c49461b6d2aad380cf92b2b07bf7d18b17ed262dec8f0e8b4adc240d7dbd59")
adr2: address_t = vlarray([uint32(0x651c6cfd), uint32(0xdc3bd605), uint32(0x7e24d934), uint32(0xf78c5864),
                           uint32(0x5b75239d), uint32(0x00000042), uint32(0x00000006), uint32(0x00000001)])
adr2p: address_t = vlarray([uint32(0x651c6cfd), uint32(0xdc3bd605), uint32(0x7e24d934), uint32(0xf78c5864),
                            uint32(0x5b75239d), uint32(0x00000042), uint32(0x0000000e), uint32(0x00000001)])
pk2: pk_t = vlarray([bytes.from_hex("6e8632d2285670a894868e180b6277d4304ef7bdf8fb13cf7fbf4cd2f44a9386"), bytes.from_hex("e747ce4dd4bad45ade6c8ea0df838fc04c578e0a48d24845720284c9d7c3a3c5"), bytes.from_hex("8f75636d7ab4fc74206c4fe1f031a6b511d41e58ed959463dff99da84a9f8320"), bytes.from_hex("f0b1ab34043e058e178152828151dffc5c871bdf6b1515b32e698291c5433311"), bytes.from_hex("70f57713a86226d3fbd98d31b74c16d400b9820f1196c323d63b441b15c44501"), bytes.from_hex("4e587f537607080ec4e658cd1f9f399a7d5d694930ba04bb433715a8a81ba63e"), bytes.from_hex("7b0cae14e29859ce30e5470c56d6c4603d5a6b8d4c96ed1824f33548d5fefcef"), bytes.from_hex("38234249fdb8bc5b06c45686a3d891a301a4ace40d0d15c3125a106d665f9600"), bytes.from_hex("0e63fde38026dfb1a30fc9916ddb7891ca52e826f91d8fe583eb111b397cf4b7"), bytes.from_hex("a8f941e214afaacc4e150fea63a449d946698156f60c6765e5207326681a57d6"), bytes.from_hex("ec025ef65c6ed48c7d41ac908de33c2820d04118f92c893589e35eca327b7e39"), bytes.from_hex("5b989fd627a6f47779c4da535a9e1cd6ecc6ead6f824917a0a0107a9884f93b9"), bytes.from_hex("c538852dfa3cbdd0ac0f37d99158c2e87aee849cf686392625d978eaf4cd42a9"), bytes.from_hex("265e8a843fbf975287d7bb3474b96260c4a4888bfadf08ee5761c223f83614a7"), bytes.from_hex("9b67bfc4060a844a5324f8e72f6f2a4500901768a9d9259fd5f1a8751cda1270"), bytes.from_hex("8183ef47bdc47e355793ad877e83ef73a37581a93e53060e7ecb884127771735"), bytes.from_hex("fc06b8a8daf976320f9e13cedfba1d21863b47c921426ab345230a1d51ee61a0"), bytes.from_hex("fee6d482eea97609bdbb736059d377a77851c98cb2bb0cbd1e76d5fb49c5e100"), bytes.from_hex("0f33ed053215fa01eb156e993c92226faa347580dbf5681c2a3fdf281d91a2dc"), bytes.from_hex("57248fa78fa857cc8b4da7cefa0864363603a9a7d350f56ecc5d806a365a27f1"), bytes.from_hex("642e32966af57e70ef75f88537f10cab8bebfe8e0059e2bbd81ca9c2a8e1fc71"), bytes.from_hex("3ce241bc15c846f57701363588f2dbdef8ce585296330f5aca267657625cf808"), bytes.from_hex("9257b7349c119aca764cb2d04533f9ef8a460a5dd8e527461eb63d42b5f0aa75"), bytes.from_hex("7cb870248c7ddc62df09c673ccfaca899139bd24e07b8770d8b166bdb60ee8d2"), bytes.from_hex("db16713c4d813e8c9cec36806a5161ba1c30576e553a772ed209f57bcd5d1384"), bytes.from_hex("74a8889ec5135359aa085f160a597f71d04d5f368550e77b3fc162a1f43b8305"), bytes.from_hex("e354d60f6ac3851ec2f4f053bd40161a37aed44cd26e1684cfaee0e300becc43"), bytes.from_hex("26aa539f676c9b7bc6bb619010c750d893d4c4c3c71d50abc4379f2c8ef87cf5"), bytes.from_hex("0d2963e25c88cc7a1960539e87b2ce811a2ba74be44f0c99bd13f4a409e458f4"), bytes.from_hex("7a6aabbee6089c69a0a443cebd20dbc16d48c89345edcc8d56fa2c00395fd993"), bytes.from_hex("9f26392f3651a161b9b54b55182d876bfe4ccd6dfa46c3f5f935a843e57c9426"), bytes.from_hex("e951cec726bf2a9aff1cd1925246b9c7eed3b6ea488d34726073a1a742c156c0"), bytes.from_hex("6c8d09d1695b0b93a7dd839ed44cf5a294d629073a4660c37e1deec3ad5f810a"), bytes.from_hex("13dbdcd00d9bdc68d653457f5c95f444f80ab0f74781bb97830d9cbdfda86bc2"), bytes.from_hex("7bc6f9cdef115791b6749e15aa635d34835a33ca042b948c72885540a550528c"), bytes.from_hex("0c718b4c0f766eb493fae19816eb999e6f0c14a29a8b7656f69ca669b646df66"), bytes.from_hex("adfa248bd7aa84be9a708c944a19482ead4684680a45ce123ce1b0defb1224b1"), bytes.from_hex("d0c708bf33b6ef0ca0fc9eb5b9aaafd6e28188d052be745f2417baebe6747b01"), bytes.from_hex("cb36f08f3bfb9004b948b30310b3d660f0534024afe71a3d90d3c5bb81782880"), bytes.from_hex("e8609ae42286601503253b8c73ef5de52d25ab00f68ac2ac5e58327a5c5742eb"), bytes.from_hex("87b22f31aa1171d210617ddf6b4cb691d4ddb2c59a2a5b834ddf854b55f2bff3"), bytes.from_hex("0f33e6411140d5c593cda3b33e6fb3c9b087d3cb360e5b20c1bfc31c312083ef"), bytes.from_hex("497d4a874145ad3775836dd134fca6f125098a253e7250137a041fe921123f36"), bytes.from_hex("0d010ef74844edc134092c15f2cd5edfa65d37e3f05c4dc16dccc6c0a4f2af16"), bytes.from_hex("ca303003c150c2fb01498e4a1d6e5b76bbc67da99abc053b7dbdf1177da67310"), bytes.from_hex("abe743bf4af3673de761ace9a6161e692421b93aacdad743df11bdbbd628359b"), bytes.from_hex("2226aa78211ddd109702d546f4e4f60b9ec84f17bef98cb19bd114459616ce85"), bytes.from_hex("bd87bd5f3b19a261857453937ce37127de05d54c4c04d94877ac8a3aba646fac"), bytes.from_hex("1a83cab147e7a1825e402d0ed39648f41a14e95ad20a26bd4b0254b4a12bc4d9"), bytes.from_hex("44f8cec87daa259a918953fbd9dadc695907cdf90c86d7a799e9c19fb9261917"), bytes.from_hex("ca758558edcacc4a92c1d3e366b4d3accb0a1fbfd71f705b7edc623ebd7286f3"), bytes.from_hex("f21efed70e2589ad2c07446696786f9b128e6ac4bffbc3b6d57022b7860bd614"), bytes.from_hex("7eb685628774a113f3bb01fae15aaa9b261bc950d01dda47dba20c283ccbed7c"), bytes.from_hex("41fe64c3ed36b59bbb7d01034c4d6f5b812ea53a61c2a93e16d0540f0ee372ff"), bytes.from_hex("f084bbda0ed179e89a609d5efd3a9347e1351d1188c408ec6546a53585cddf6d"), bytes.from_hex("5df008c5a21d7919cd51fd5595a3250c22f75e9838780e52a5c04fecff42498f"), bytes.from_hex("4c7f2a1ed885e29f0a19222e5ee91417b492fc0eec4acdffa07bdec699701ba0"), bytes.from_hex("9071f2a3359c705ca3ad78fb5270b8f326d89b2b5cb1464e8c4c2769d84e084d"), bytes.from_hex("67bd563ef96f3dd2ac378df2b00ee14573fd652f13c11a2de575b6f91d677861"), bytes.from_hex("a4a1e28c831e0a6985a1d17fbcdf4dc742310cee43e959d79e23d390110fd5af"), bytes.from_hex("bd0c79086419d07d46839f87b6f2424eb9cd48df33595b67c899616a933fb3a5"), bytes.from_hex("aaa35616f7071d8a17038c324c81ab0a713af78352e4e552772f88e98fac88f7"), bytes.from_hex("227a9f8e0dde29e67e2289e3d1fd62332c7659eb0819ea6f1f7749b484a76667"), bytes.from_hex("f9d84ca201f12138201e17d5c5445c96d812d4c13e9691dc047d1141d9774aca"), bytes.from_hex("018e92ad07fad5c923e721b26bef79398e5c31f05ccdf715b45480606bba08b9"), bytes.from_hex("5ffbe159ea55a6b4d613a6320342b63cb5d0b71d438d38e487a3726f765f1714"), bytes.from_hex("5b1c1ed296f0cb7d9ede3ea79a5aeb34d44ed2dec12c1069e299c51081c47e62")])
sig2: sig_t = vlarray([bytes.from_hex("292a80929c4566fb5fd8f88e025be75dde7908b66bdceadd93a1c6d867afa04c"), bytes.from_hex("baa5331c56a35bfb826edcac4f8e9a665576fe2becb032a1020e8e066677cf30"), bytes.from_hex("a8e595daa578b2e0299b03bf4a45bde40c9effa067d53c965bb14e78d79b731a"), bytes.from_hex("2639342b334f45a92654da04c923e54e9c87a03ecfc7f8d6012940f1962dd06d"), bytes.from_hex("db791a35a4515ce13d426e01db55cc4b7119cdc48220b1ad03d3ac6675d80c1a"), bytes.from_hex("771bb23be4b8aed0479c996a6de61b9e47f3c2b41837801e9287d3b51df8c533"), bytes.from_hex("204f2d6027a423a285c2b48a5740c370feb10b02bb267d76ad0d13aaaaf1368b"), bytes.from_hex("38234249fdb8bc5b06c45686a3d891a301a4ace40d0d15c3125a106d665f9600"), bytes.from_hex("3596daca60b1ab6ce4172ea6ba83512145e2179e68221754228d7313709331d3"), bytes.from_hex("db21b578c469e1ad0f65ec229c5d1bfe902af7f303891db2947ab214db3e7d74"), bytes.from_hex("ec025ef65c6ed48c7d41ac908de33c2820d04118f92c893589e35eca327b7e39"), bytes.from_hex("bfa2d10698bb2962d9e6da682acf5c94b6e2dbdc122c1b780ba6cd7cc3ba9002"), bytes.from_hex("ab296122fd3e3ea2cef043db34cb6ac1130719fdb9074e8e9726ad46953a0c8c"), bytes.from_hex("7793ad30e3a050c0535a1cc905af3443d3578c388e5ddcb3194772bb3bb6e56b"), bytes.from_hex("9eede69b8446e70f6e7169799bc1910bf7ea512a91e53ace9855c54be0af52b0"), bytes.from_hex("1425e1e08cf347a0175f963e6692907616c3447cf3b4f2c62fff0fdb8df2bb19"), bytes.from_hex("0cb4495216f8c396032f4fe5b2364378bf834c638c17c629e9c6a9a6740a2b7d"), bytes.from_hex("f8dddf7cf9bc577d9047426fe5d2214ecd772537fd64ba5709c0e38b6cf88621"), bytes.from_hex("f031761a8f76644495e8591fe100ee0a17abcc3ebea2e61b9abc8359b46d9323"), bytes.from_hex("79c094ad4517f67e1ce6dce8fab295037b6ac8a96b1642da72e90eaa0145b497"), bytes.from_hex("6cfe6be5f12ab1030281302b54c5e6ebfff7c037a9fa75e5c3c0dea6cf858270"), bytes.from_hex("249abc3bed98942d74cf0a9029f3e22497272afb3491a812eeb66b4f964c21b5"), bytes.from_hex("f0a08581de8f97ff5ee6e04dcd199b13d93df95ae5f548df67d2cd60ce5bb6f3"), bytes.from_hex("9a6b7790b74bb324314677ab4ec9d429600355b23553bb99fed9f1bc8a1f8fbf"), bytes.from_hex("bb315a2ce59b758e2ad735edf9e78f457e24d883ea8dcecbcbb4d92ccc27eef7"), bytes.from_hex("e1f6a33427a63cef6b8d965be6ed6941ddf7a4786e6f2c2291bb7c3a41e88fcb"), bytes.from_hex("14d356656d7eed849c12f4ee2a44fd0ef5125040885628c3517b9216cf12a2c6"), bytes.from_hex("26aa539f676c9b7bc6bb619010c750d893d4c4c3c71d50abc4379f2c8ef87cf5"), bytes.from_hex("e4a1bf9e8a7e2c9d89e2986aff8c081a2e0d5a329c8737e6c2b61cfca7099b1c"), bytes.from_hex("56b87944928de5a770a8ec42ba5ad28dd13f3e3946181959c2c55d993522a327"), bytes.from_hex("503eb5ef36933dc90a65ff597196625bce15bc7fd2124a61a40c377487169811"), bytes.from_hex("28f39c043ef3902f5bcbff1a4f04e982cccc9d9cc32eb29d79cbd25eddfaf70f"), bytes.from_hex("329c675374277c29b3d35382b2544b2a7df3aae9dd5107a93540d1fd8e467ced"), bytes.from_hex("bd65c5613d6dc3ef8fe739ff5d9e54b9b8a6e615d850b6dadc2ac62ad621e8ab"), bytes.from_hex("18132689a63ecea60e51c9107e089e9fd42a8d8518601f56f9138c0d5cca70c2"), bytes.from_hex("26d1e76bacc0d1c8dcbd57b71320acf1f8843d9c3fb8323cc3d9d54e1961cadd"), bytes.from_hex("dcada1b0ab17b375b65eb7d16d25068bc14f3e09ded9aac9d946c5bac5c29176"), bytes.from_hex("b830e6b5c19e34f103b3c1ac9dc5acb0fe92aa6d571c0f1ab4e4d5d5af72104e"), bytes.from_hex("d4e56cd11824d0171620e7dd91792f23e969ebfb2bca32da0a7f338fc0584a63"), bytes.from_hex("f15255d1d9ef865bc6724e5d9d542380ef122342ec5651be74c06220054b7f77"), bytes.from_hex("eaa89e9457de6acbbdbf04ac6aadfbd91a6c16098d2e382d3ddea8239ac9b5fb"), bytes.from_hex("2f1ec24749c57caf58df878eceb22c94c260ebb4a6fcd3a847b1e03a670dd7af"), bytes.from_hex("0b0a696b08950a023bcbbe4d8a31f3e8c79b19be8efefe16412f92080d358d3d"), bytes.from_hex("a2a42471842f3e4163f86fc558473236f7ca1df695258c5e2902e59c17938c42"), bytes.from_hex("4eb9dcd804572b670cc3953d8900a035ec2a02b1c45d0cdbac86738423a0b34d"), bytes.from_hex("deb00ad5468e448534ceea95304352fd68ea45612deb5d7b657b1a169ba00a70"), bytes.from_hex("3d3bd1a6ae9ea6027a4070bb248218c38346d1d424864bd88c4007a7e637169b"), bytes.from_hex("d41deb305f3abb70e7f9589f948d42ba4f5420b1016d08083f416cc96ed1dfbb"), bytes.from_hex("5840f945cbee6036016fdba69f4304c5bdb9bc4f042a3848f2812f9027f9d39e"), bytes.from_hex("e282a8a7fb25c6d83ae2e4211b9b39ffa96d2c0d37c28ea7494ac1fe347e70ed"), bytes.from_hex("806ec329f11b592b579e3ffe1269164cabff581ebb4ebfeff1503c657d58b8be"), bytes.from_hex("758c7b0d9ac5cdc6283a95099c9b7eed6b15c0105150792b6daea213f7d0b013"), bytes.from_hex("e515e18d50228fd30d0aa9fa54bcce26a6182fd540e0f4750522ebeb0a3a7ad6"), bytes.from_hex("601a2a8bf88c04d21445e6aa066d8ee2998b6ff3aee8ee6089ea85043f669a63"), bytes.from_hex("cc952843ccdfca2b4075615ad1c4f3dd052a02151d3f240b1d646eb69155a3a6"), bytes.from_hex("c2e4f0a0adad2cae4b818bece1ff2d4256f0539787f244d628d6b7bdaee5e952"), bytes.from_hex("f1292f7465e633d650527a6b05d42b4af3d1e50376210c82d1bd4f978cea4874"), bytes.from_hex("2177b6e8b7b1075b2541e29dcfcbad51cf1001a85131ea15195c4e955ac87aef"), bytes.from_hex("67bd563ef96f3dd2ac378df2b00ee14573fd652f13c11a2de575b6f91d677861"), bytes.from_hex("2fc343b8351f715eace039f599aa50a05618eaa6ac716f25915be80130fb6b9e"), bytes.from_hex("581fb59eeaa5e5083fa209203f66606014250156ecbcc79002345167a49e8ecf"), bytes.from_hex("e2601d362f6dee846849c9381d44a2c80a8309a75b8f7f3c370c76c126c69185"), bytes.from_hex("03266024b3e1438a53e9524eff045a1087520dfe4fd131d1f962f3b4a14352f0"), bytes.from_hex("24fc2ad67e8c2aa7f6e6837922f5f9c937a04c99ef168af9fce78107ac463b5d"), bytes.from_hex("85d8b1a53e6151a5c0ce583989bf6fb9d9174c063b5b13100ea9aa4f09a16ac5"), bytes.from_hex("546bcdfa36294c2aaad3706c7abfed69d76511c2bbd84d471ea0c2f9a8a3248a"), bytes.from_hex("ef81bd7985c6a6c1386eed60e243c4c2e38d3be4911a8ead042b2f2b5630ef75")])


def verify_pk(pk1, pk2):
    verified = True
    if len(pk1) != len(pk2):
        print("pk2 has wrong length")
        verified = False
    if verified and pk1 != pk2:
        print("pks aren't equal: got " + str(pk1) + " expected " + str(pk2))
        verified = False
    if verified:
        print("Signature verified")
    else:
        print("Verification error :(")
        exit(1)

def test_wots_kat(m: digest_t, pk: pk_t, sig: sig_t, adr: address_t, seed: seed_t, adrp: address_t):
    pk2, adr2 = wots_verify(pk, m, sig, adr, seed)
    if adr2 != adrp:
        print("adr is wrong after verification")
        print("got: "+str(adr2))
        print("expected: "+str(adrp))
        exit(1)
    verify_pk(pk, pk2)

def test_wots_self():
    adr = array.create_random(nat(8), uint32)
    seed = bytes.create_random_bytes(n)
    msg = bytes.from_ints([0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
    msg_h = sha256(msg)

    sk, pk, adr = key_gen(adr, seed)
    sig = wots_sign(msg_h, sk, adr, seed)
    pk2, adr2 = wots_verify(pk, msg_h, sig, adr, seed)

    verify_pk(pk, pk2)

def main():
    print_dot()
    test_wots_kat(m1, pk1, sig1, adr1, seed1, adr1p)
    test_wots_kat(m2, pk2, sig2, adr2, seed2, adr2p)
    test_wots_self()
    test_wots_self()
    exit(0)


if __name__ == "__main__":
    main()