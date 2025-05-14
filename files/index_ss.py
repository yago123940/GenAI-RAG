import requests
import os
import json
from dotenv import load_dotenv
from auth_ss import singlestore_auth
from hashlib import sha512

load_dotenv("config.env")


conn = singlestore_auth()

# Dados a serem inseridos
data_to_insert = [0.018540628, -0.087611735, -0.13531698, 0.0036451179, -0.10187034, 0.017454058, 0.06422777, -0.041748133, 0.027332213, 0.03770613, -0.04282903, 0.037560977, 0.063499354, -0.011164627, -0.021797763, -0.0033811585, -0.013848197, -0.024132907, -0.026715245, -0.15323925, -0.08433963, 0.096769325, -0.03454326, 0.057766017, -0.12451567, 0.068532705, -0.09646382, 0.019938298, -0.018839326, -0.06952322, -0.012272129, 0.00022688707, 0.024728168, 0.019640984, 0.089352086, 0.044246852, -0.05105838, -0.06200131, 0.0027018609, -0.06944551, -0.04230338, 0.013092992, -0.036010087, 0.019895751, -0.024583623, -0.024524745, -0.05627777, -0.023537857, 0.010607929, 0.020648008, -0.03258565, 0.009432452, -0.0047378847, -0.026821848, -0.020911124, 0.07515372, 0.012451221, -0.024445895, 0.02021341, 0.015791371, 0.046285786, -0.018375985, -0.02516524, 0.019213824, -0.09125155, 0.061656486, 0.025105111, -0.005806275, 0.011659118, -0.00054518634, 0.010829375, -0.0004797851, -0.02114857, 0.06503543, 0.033206422, 0.036305394, -0.0519493, 0.0064676614, 0.031625614, 0.017373463, 0.012224819, 0.038273126, 0.048683032, 0.01181054, 0.018165516, 0.053364635, 0.08071168, 0.018912727, -0.026587786, 0.006141562, -0.06990329, -0.071559235, 0.0956435, -0.019272493, 0.019903177, 0.023613203, -0.030693365, 0.08762865, 0.08338948, -0.023772644, -0.037182212, -0.00874465, -0.015385064, -0.030114345, 0.110742666, -0.0450946, 0.036328655, 0.004008433, -0.02673884, 0.054997634, -0.017703017, -0.0021664621, -0.0010005881, -0.0017130942, -0.015974917, -0.025580367, 0.0074725403, 0.046082135, 0.012069365, 0.04503576, 0.013803167, -0.0032032456, -0.059605915, -0.028043378, 0.006323328, 0.018658552, 0.019212173, -0.102071114, 0.014058904, -0.07453529, -0.09377132, 0.027590407, 0.022054184, 0.042862896, 0.019388003, -0.033115957, -0.041595105, -0.03555302, 0.072744325, 0.020517029, -0.017165683, -0.032082915, 0.0013232041, -0.003626653, 0.0053699333, -0.02666144, 0.037744317, -0.07873833, -0.049738828, -0.035967983, 0.015553591, -0.006918771, 0.012644322, -0.026173793, -0.021800142, 0.05138934, -0.014789311, 0.04792962, -0.0117973685, 0.014084157, 0.020674936, -0.028556129, 0.04893083, -0.047154855, -0.018928379, -0.0094126975, 0.04318356, 0.052520342, -0.009814507, 0.010174751, 0.022565592, 0.018472446, 0.025334226, -0.00048859586, 0.002134698, -0.030816104, -0.012652738, 0.016518986, 0.0152928205, 0.025305234, 0.00046516588, 0.056915093, -0.0021129234, 0.026389165, 0.0826276, 0.014437218, -0.025976077, -0.0016976892, 0.0560712, -0.11234124, -0.0022579972, -0.046977926, 0.009968968, -0.042404115, 0.0685434, -0.04069832, 0.0044481773, -0.04048065, 0.16518225, 0.03558913, 0.023169119, -0.03304531, 0.006658045, -0.0034073924, -0.02359982, -0.023895498, 0.00060497166, -0.07860338, 0.020766996, 0.047823764, 0.00380822, 0.025953395, 0.051306337, 0.0370793, -0.017457483, 0.017863832, -0.0043882504, -0.05625724, 0.067151316, 0.013053221, -0.04209354, 0.014235296, -0.006347048, 0.013876784, -0.014096989, -0.017050087, -0.026218627, -0.048953906, 0.0010360393, -0.01462956, 0.076200984, 0.0073886914, -0.052416377, 0.030896047, 0.040504977, 0.039029326, 0.017812084, 0.026972767, 0.0002414554, -0.051768035, -0.007234235, -0.061083898, -0.04446902, -0.040944368, -0.0046821446, 0.00069425907, 0.03788321, -0.030574352, -0.020618262, 0.06919624, -0.015546632, 0.034979284, 0.0021282726, -0.09339556, -0.04059494, -0.039491, -0.004397401, -0.013098751, -0.056290112, 0.026752781, -0.026333524, 0.03630655, 0.02432557, 0.040203657, -0.016834082, -0.018150013, 0.018969169, -0.014582204, 0.053411942, -0.0141519, 0.0002883842, 0.014991729, -0.016232045, -0.0023607914, -0.015248746, -0.041643273, -0.013608098, -0.0027114267, 0.047488164, -0.013532093, -0.027644372, -0.033792973, -0.01530243, 0.025840899, -0.026597753, -0.02140292, 0.030268712, -0.011008043, -0.05665428, -0.010838584, 0.034280784, 0.016932147, 0.030417018, -0.021918671, 0.06344647, -0.056843616, 0.020030469, 0.003639612, -0.007496419, -0.0133957425, 0.0030616857, 0.051142093, -0.00863358, 0.02865018, -0.0008042072, -0.0038851365, -0.031070882, 0.008524089, -0.035430823, 0.0033515322, 0.05557886, -0.011138437, 0.0103174085, -0.015939508, 0.058985535, 0.045690067, -0.030681571, -0.0024488592, 0.038024608, -0.030331874, -0.027519226, -0.027634997, 0.0716945, -0.024725508, 0.06901921, -0.034979086, 0.03707953, -0.027274042, -0.03652347, 0.009913548, 0.030741438, -0.054191235, -0.01895252, 0.014056505, -0.007121903, 0.02094932, -0.020374333, 0.05885104, -0.020551892, -0.03621956, 0.014736663, -0.008000686, -0.062962584, -0.04040817, -0.0020746863, 0.021979952, -0.038753383, -0.020488825, 0.0037641593, 0.0406019, -0.0104035465, 0.01967227, -0.011974448, 0.0035400947, 0.028130254, 0.050543662, -0.015371979, 0.007735587, 0.013076225, -0.019314827, 0.03127702, 0.0018202539, 0.027190518, 0.027305314, -0.06878049, 0.049743388, 0.0138142025, 0.0283111, -0.056029394, 0.058945887, 0.034775756, 0.07487876, 0.024668995, 0.018105198, -0.02486486, 0.011861592, 0.045274336, -0.026271844, -0.029855197, -0.00015328915, 0.0061588343, 0.047281798, -0.011387404, -0.024944782, -0.03197078, 0.019588709, 0.009939841, -0.0022433244, 0.015386243, 0.0034824824, 0.020623878, -0.013280783, 0.02310614, -0.002013677, -0.0049664946, 0.012215678, 0.0033502982, 0.011443235, 0.03699778, 0.02634487, -0.021052806, 0.038622662, 0.0022810844, -0.033886638, -0.016846789, -0.0054179262, 0.010627226, -0.0075350725, -0.01593995, 0.0019044221, 0.011628856, 0.034707334, -0.035722625, 0.024845418, 0.0027753606, 0.0028343592, -0.0028497034, -0.002136246, 0.011258213, -0.015859302, 0.0032420226, 0.035315286, 0.04063495, 0.008766618, 0.042677574, 0.0039506806, -0.03354414, 0.0035214883, -0.04992951, 0.04455538, -0.02493171, 0.002011248, -0.04621541, 0.040646736, -0.032696776, 0.06371928, 0.0036563082, -0.03825863, -0.03570317, 0.0063864295, 0.028999614, 0.009231654, 0.02130772, -0.018923748, 0.039323542, 0.032947276, 0.012457424, -0.021189641, -0.0036498616, -0.032354895, 0.027591065, -0.022145318, -0.022725426, 0.040141825, -0.0112715, -0.03656197, -0.021421095, 0.023206964, 0.01911408, -0.01610853, -0.0073744883, 0.0043995627, -0.028208539, -0.0026392087, 0.022200827, 0.0050943466, 0.019322122, -0.026913198, -0.045169555, 0.019182067, 0.026162786, 0.013852444, -0.0046103625, 0.009294909, -0.00251137, 0.03455265, 0.031099126, 0.038195416, 0.015821753, -0.025492107, 0.015367123, -0.017940328, -0.025628826, 0.008249928, -0.043704465, 0.015349117, 0.004054388, 0.015775193, 0.034092437, -0.005956957, 0.0015528122, 0.06699687, 0.03445086, 0.051904052, -0.0020058062, -0.0096298065, -0.036520828, -0.01270497, -0.012219381, 0.047221906, -0.028146228, -0.006265736, -0.044581674, -4.5625544e-05, 0.026151678, -0.041690525, 0.0024077585, -0.024153227, -0.046054635, 0.010606723, -0.015818909, -0.0033235124, 0.032254476, 0.014005567, 0.029454095, -0.025011552, -0.016971247, -0.02255741, 0.012282636, -0.009935356, 0.01864768, -0.036618736, 0.018117676, -0.0017328231, -0.039240405, 0.054905158, 0.029155733, -0.006066835, 0.012427332, -0.02439021, -0.027167924, 0.015573892, 0.048483383, -0.021442613, 0.0027464193, 0.00078180153, -0.017782979, 0.013177587, 0.020836871, -0.023520665, -0.03183618, 0.00284293, -0.014578621, 0.005970094, 0.038648833, 0.004828773, 0.017440451, -0.03186979, 0.014096759, 0.09244598, 0.036485072, 0.049490362, -0.037606854, -0.04591455, -0.0039727273, 0.012966018, -0.039536837, 0.025291678, -0.0050884634, -0.029461656, -0.06474398, -0.033494726, 0.016916249, 0.025811778, -0.021681434, -0.02431353, -0.01922598, 0.023780625, 0.005296247, 0.014609217, 0.04993122, 0.0017772048, 0.043509442, -0.019530967, 0.004745962, 0.00023662325, 0.0046535614, 0.0005757467, 0.010133495, 0.0018789032, 0.041887067, 0.008591789, 0.055362698, -0.019919883, 0.006354068, 0.015699008, 0.0064460034, -0.01654288, 0.0043834965, -0.028222568, -0.0077001676, 0.027347833, -0.023837289, 0.00539567, 0.014051477, 0.008860594, -0.02812528, 0.011169831, -0.0006635996, -0.007203779, -0.0010398851, -0.020394037, 0.007965771, 0.0017857556, -0.008021044, -0.0076986714, 0.03058818, 0.022283943, 0.008714208, -0.014024302, -0.027745739, -0.013356223, 0.035951477, -0.006089925, -0.014031284, -0.046949856, 0.016512278, -0.014745143, 0.013255791, 0.04599195, 0.017691223, -0.03280651, 0.015994556, -0.043713283, -0.040761948, 0.033172406, -0.005850985, 0.02342961, -0.032978527, 0.016232891, -0.024666881, 0.00036889417, -0.021814177, 0.015557609, 0.027201016, 0.009265541, 0.020014726, 0.010948622, -0.0029185435, 0.032874975, 0.020891663, 0.03007713, 0.021647364, -0.0061102663, -0.052415974, -0.011719019, -0.009255238, -0.011302315, 0.0020719373, -0.026871242, -0.05551537, 0.013400774, -0.037464283, 0.0023321589, 0.0063914116, 0.014905965, -0.013031189, 0.012753028, 0.028091203, -0.019720377, -0.030412868, 0.016339606, -0.04763384, -0.0025596467, -0.022224614, 0.009181239, -0.021814715, 0.020862767, 0.0059010554, -0.014282335, -0.014951593, -0.006823445, 0.017071178, -0.0388886, -0.010685192, -0.015834212, 0.013791049, 0.021235408, -0.026859164, 0.032999005, -0.014456687, -0.028647352, 0.023045069, -0.016234396, -0.010998687, -0.034366712, -0.034601737, 0.014421988, -0.027789317, 0.014406574, 0.044851888, 0.023101268, 0.011838677, 0.036289837, -0.024133712, -0.02940667, -0.018649265, 0.03147146, 0.04650443, 0.02816297, -0.021184633, 0.03484705, 0.01963117, 0.011438396, -0.04207237, -0.040486984, -0.039927945, -2.176479e-05, -0.0045624096, 0.03259726, -0.009624032, -0.035660073, 0.008810971, -0.0020714856, -0.022400275, 0.016492046, -0.05397077, -0.009882033, 0.00769427, 0.03972083, -0.028837243, 0.014203874, -0.000708436, -0.027130572, 0.014266354, -0.010825995, -0.04724585, -0.015408015, 0.023609523, 0.011756152, -0.016918385, -0.009130472, 0.022630567, -0.0014508726, -0.022604764, 0.0111225, -0.020270614, -0.019096043, 0.026776213, -0.0032268255, -0.032699417, -0.012312455, -0.04053154, -0.0030926873, -0.023028119, 0.025200201, 0.03677788, 0.0085892705, 0.028315319, -0.033737127, -0.016633412, -0.029799115, -0.015234329, -0.0030381805, 0.021581743, 0.024307402, -0.04087265, 0.0013177005, -0.0073194243, 0.026738966, 0.0029669649, 0.006652636, 0.030068165, 0.017142188, 0.041418836, 0.05981168, -0.0030449445, 0.009352236, 0.015752826, 0.002412132, -0.0008271186, -0.042161178, 0.02543749, 0.025419928, 0.015397842, 0.0071448213, 0.004194366, -0.0062538255, -0.0058898632, 0.011470045, -0.072762266, -0.015304616, 0.020820383, -0.009554144, -0.0051184823, 0.022706263, -0.024549155, -0.0069955476, -0.019754156, 0.0015278189, -0.00564578, 0.00066055777, 0.006739199, 0.02164164, 0.02536602, 0.017508175, 0.02502872, -0.0060946285, 0.024590727, -0.02302302, 0.00480393, 0.024560666, 0.005966336, -0.009983926, 0.0061157513, -0.00037700593, 0.016743012, -0.00095463294, -0.030908046, 0.009101238, -0.009694844, -0.002013046, 0.006376991, 9.34601e-05, 0.013611359, -0.007566884, 0.007917085, 0.0067034964, -0.0064000166, -0.03366909, 0.019488458, -0.022031136, 0.012034595, 0.005789037, -0.00031708227, 0.026146278, -0.0035424961, 0.004158568, -0.00069859304, 0.019103646, -0.006167797, 0.014817855, 0.016994199, -0.016285848, 0.020089962, -0.0230395, 0.025060944, -0.02931689, 0.035396762, -0.0029717218, 0.0036355364, -0.028364455, 0.013579987, -0.031983975, 0.020215703, -0.04190426, -0.04629377, -0.030303467, 0.025584573, -0.0456116, -0.021663353, 0.022342665, 0.015128764, 0.024345586, 0.01544516, -0.03785251, 0.0074997344, -0.026668357, 0.011621227, -0.009190459, -0.024719624, 0.036156658, 0.0031726717, 0.0021658093, 0.019234205, 0.013713678, -0.009495908, 0.015973592, -0.019956581, 0.018913366, -0.00024848097, 0.0048020757, -0.044577576, -0.003577327, -0.0075722183, 0.013466056, -7.0755406e-05, 0.016351458, 0.017936317, -0.0326254, -0.006331627, -0.027778035, -0.0051359753, 0.007519593, -0.031091496, 0.00045338576, 0.014704408, -0.0011365502, -0.042245883, 0.01898619, -0.02417777, -0.004694161, 0.00832976, -0.02348878, -0.0068651256, -0.035685193, -0.018668419, 0.02730494, -0.018494021, -0.010222304, -0.009668643, -0.0075488104, -0.031120362, 0.010808072, 0.018081538, -0.004527435, -0.023553126, 0.012149045, 0.032578103, -0.007460604, -0.015282749, 0.023066055, 0.030247178, -0.014606773, 0.0053117555, -0.022414137, 0.033223856, 0.00054538145, -0.033448882, 0.00030928903, -0.011564863, -0.012721873, -0.0052529154, 0.014889969, 0.0016008496, 0.03275638, 0.026363388, 0.023831826, 0.0032725993, 0.016112037, -0.01188141, -0.01932038, 0.014840983, -0.0045570037, -0.013507802, -0.011369197, 0.013537627, 0.007953318, -0.018066099, 0.047822643, 0.029708968, -0.01118136, 0.0012923612, 0.02190796, 0.0061109923, -0.010917664, -0.030644925, -0.021190433, -0.036572516, 0.035904408, 0.036539458, -0.01567624, -0.011484577, 0.027037105, -0.031243604, -0.0117730275, -0.0121896, 0.031499367, 0.007066294, 0.0130010815, -0.012687419, 0.03831832, 0.0038122134, 0.038356543, 0.025940558, -0.047849935, 0.015448988, 0.036533542, -0.052528635, -0.028036684, 0.014103495, -0.0062247734, -0.014860887, -0.026162725, 0.01688176, -0.011781939, 0.011572676, 0.017189695, -0.005885092, -0.047562286, -0.016160334, -0.030058643, 0.0015276294, -0.051812198, 0.025680967, 0.02452755, 0.034063045, 0.022446133, -0.00085866096, 0.029021729, 0.04801566, -0.0003877112, -0.020107739, 0.03223221, 0.004189149, -0.016916761, -0.055125646, 0.005481779, -0.022069138, 0.00073717313, -0.0034406686, 0.016960895, 0.0010673905, 0.0075044096, -0.008972616, 0.010685956, 0.004346342, 0.018918455, 0.014298626, 0.0006297716, 0.011968121, 0.020664012, 0.0038631053, -0.003877138, 0.03633309, -0.011591189, -0.0033656955, 0.016444476, 0.025605097, -0.00028014876, -0.022731723, -0.010997064, -0.010676157, -0.0070191347]

text = """4
Uma das primeiras decisões dos investidores, quando estão montando uma
carteira, é sobre a alocação: quanto deve ser direcionado para renda fixa,
ações, ativos alternativos (como criptomoedas), mercado local ou global?
Essa “divisão do bolo” precisa estar relacionada com os objetivos de cada
um – mas também alinhada com o cenário para a economia.
O rumo dos juros americanos deu a tônica dos mercados em 2023 – as
taxas nos EUA ainda em alta no primeiro trimestre afetaram os ativos de
risco de países emergentes, como o Brasil. Mas, da metade do ano em
diante, a percepção de que o pico já havia sido atingido lá fora, aliada ao
início do ciclo de queda da Selic (taxa básica de juros brasileira) por aqui,
impulsionou um rali de respeito.
O Ibovespa terminou 2023 com alta de 22%, enquanto o CDI (taxa de re-
ferência para a renda fixa) acumulou 13%.
Para 2024, a trajetória dos juros americanos vai continuar fazendo preço.
O Brasil tende a se beneficiar em caso de redução, o que atrairia recursos
de investidores globais. Já no lado interno, a Selic – hoje em 11,75% – pode
chegar aos 9%. Esse movimento tende a valorizar as ações e também os
títulos de renda fixa prefixados, se a queda for além do esperado – já que
quando a taxa cai, o preço do título sobe.
A carteira ideal para
ganhar e se proteger
Clique e assista ao painel
5
A inflação brasileira promete seguir na meta – embora para Caio Mega-
le, economista-chefe da XP, ainda não se pode afirmar que ela esteja
completamente dominada. “O BC vai continuar cortando os juros, mas vai
manter a cautela”, diz. Uma Selic abaixo de 9% só virá se houver confian-
ça de que a inflação voltou para níveis normais.
Renda fixa, ações ou multimercados?
Como a Selic chegando aos níveis previstos, Catherine Cruz, CIO da Integrity
Wealth Management, considera que a renda fixa segue sendo um bom in-
vestimento. “Os títulos indexados à inflação são os nossos preferidos, espe-
cialmente os isentos”, explica. “Observamos empresas sólidas pagando até
IPCA mais 6,5%, uma das maiores taxas dos últimos cinco anos.”
E, nesse cenário, como ficam as ações? Investidores questionam se a
alta de 22% do ano passado significa que há pouco espaço para novas
valorizações em 2024. Ronaldo Patah, estrategista de investimentos para
Brasil do UBS Wealth Management, considera que os ganhos devem per-
sistir, já que o fluxo estrangeiro que impulsionou o Ibovespa nos últimos
dois meses deve se manter ao longo do ano.
Os multimercados são sempre recomendados por conta da flexibilidade –
e assim continuam para 2024, mesmo considerando que no ano passado
o rendimento da categoria (de 9,3%) perdeu para o CDI. Para Patah, ainda
é importante manter parte do patrimônio (20% do portfólio) nesse tipo de
ativo para proteger a carteira.
Diversificação geográfica
A diversificação geográfica também é uma prioridade para os especialistas
– afinal, pode ajudar a reduzir riscos. Com a tendência de queda dos juros
em 2024, a renda variável nos Estados Unidos volta a merecer espaço na
carteira, considera Patah - especialmente as empresas de tecnologia en-
volvidas em projetos de inteligência artificial.
O mesmo vale para os
bonds, títulos de renda fixa emitidos no exterior.
Mesmo que o mercado espere o início de uma queda dos juros nos EUA,
as taxas alcançaram o patamar mais alto das últimas duas décadas no
ano passado – o que significa que ainda serão atrativos.
% ao ano mais IPCA é o que pagam títulos
de renda fixa de empresas sólidas6,5
6
Ibovespa: novos
recordes ou correção?
O ano de 2024 tem potencial para ser positivo para a Bolsa brasileira,
ainda que de forma menos intensa do que o ano passado, quando o Ibo-
vespa fechou em alta de 22,28%, em sua maior pontuação nominal da
história (134.185 pontos).
O principal motivo para o otimismo é a esperada continuidade do ciclo
de quedas de juros no Brasil e Estados Unidos, possível graças ao recuo
da inflação.
O Fed (banco central americano) começou a elevar os juros básicos em
2022 e só no fim de 2023 o mercado entendeu que não haveria mais no-
vas altas - a expectativa é que as taxas comecem a ser reduzidas após
março de 2024. Com esse cenário, os ativos de renda variável, como as
ações, são beneficiados.
O otimismo também é impulsio-
nado pelas baixas cotações das
ações brasileiras, quando compa-
radas aos papéis de fora e mesmo
aos próprios patamares históricos.
Quando se leva em conta não a
pontuação nominal do Ibovespa,
mas sim o indicador preço/lucro
(P/L) das ações que compõem o
índice, isso fica evidente.
Aos 130 mil pontos, o P/L do Ibo-
vespa é de 8,5 vezes - sendo que
a média histórica é de 11 vezes,
calcula a Santander Corretora.
Santander
Bradesco BBI
Guide
Genial
Bank of America
Itaú BBA
XP Investimentos
Inter Research
BB Investimentos
Ativa
Média
160.000
157.000
155.000
151.200
145.000
145.000
142.000
142.000
141.000
138.000
147.620
Casa de análise Projeção (em pontos)
Fonte: Instituições financeiras
As projeções dos analistas
para o Ibovespa em 2024
Clique e veja as projeções
completas para o Ibovespa
7
As ações “queridinhas”
para 2024
As perspectivas para a bolsa brasileira em 2024 são positivas – mas in-
vestidor que se preza sabe que o desempenho dos ativos não é unifor-
me. As ações escolhidas com mais frequência pelas casas de análise nas
carteiras recomendadas podem dar uma indicação das candidatas a se
sair melhor ao longo do ano.
Nessa lista estão duas empresas que podem valorizar por processos de
privatização (Sabesp e Copel), uma companhia beneficiada pela redução
dos juros (Localiza) e uma produtora de commodity (Vale).
A expectativa com a Sabesp (SBSP3) é positiva pelo avanço do processo
de privatização. A Ativa Investimentos, por exemplo, espera que a venda
da companhia para o setor privado destrave valor e aumente a eficiência.
“Uma vez privatizada, espera-se que a cultura da Sabesp mude, com
melhora na eficiência, na geração de caixa e na margem de lucro”, afir-
ma Pedro Serra, chefe de pesquisas da Ativa. A estabilidade do setor de
saneamento, pouco dependente de ciclos econômicos, também favore-
ce a empresa.
Com a Copel (CPLE6) – empresa de energia do Paraná, privatizada em
2023 – o pano de fundo é semelhante: agora nas mãos do setor privado,
a eficiência da empresa deve aumentar, seja pelo corte de despesas
operacionais ou pela concentração nos seus ativos-chave. Espera-se,
por exemplo, que a companhia venda a Compagas.
SBSP3
CPLE6
RENT3
VALE3
Sabesp
Copel
Localiza
Vale
35,61%
36,05%
23,00%
-5,73%
TickerEmpresa Retorno em 2023
As ações mais indicadas para 2024
Fonte: Santander, Ativa Investimentos, BTG Pactual, XP Investimentos, Ágora Investimentos, Guide e Economática
Clique e veja as recomendações completas para 2024
8
A continuidade do corte dos juros aqui no Brasil é o que embasa a
recomendação de compra de ações como as da Localiza (RENT3),
que tem 85% da sua dívida atrelada ao CDI (taxa pós-fixada que
acompanha a Selic).
Outros pontos que fundamentam a preferência pela locadora é a melhora
do horizonte para o segmento de veículos seminovos e o fato de as ações
estarem descontadas em relação ao
valuation histórico, diz Ricardo Pe-
retti, estrategista da Santander Corretora.
Já as ações da Vale (VALE3) são indicadas por conta da revisão para
cima dos preços do minério de ferro. O BTG Pactual, por exemplo, es-
pera um aumento da produção e das vendas da mineradora, assim como
uma queda de custos.
Outras ações – como Itaú Unibanco (ITUB4), Equatorial (EQTL3), Mer-
cado Livre (MELI34) e Prio (PRIO3) – também foram citadas com frequ-
ência pelas casas de análise consultadas pelo InfoMoney.
pontos
é a média das projeções de
nove casas de análise para
o Ibovespa em 2024
147.620
Clique e assista ao painel
9
Dividendos de ações
ou FIIs: que tal ambos?
A estratégia de investir buscando o retorno com dividendos – sejam eles
pagos por ações ou por fundos imobiliários (FIIs) – é uma das preferidas
pelos investidores que desejam receber uma renda recorrente e contar com
carteiras mais estáveis. Afinal, embora os dividendos e juros sobre o capital
próprio (JCP) variem de acordo com o desempenho das empresas e dos FIIs,
essas oscilações geralmente são menores que as do mercado em geral.
Em 2024, tanto os FIIs quanto as ações devem se beneficiar da queda
dos juros, que tende a valorizar as cotações e elevar os lucros. Vicente
Guimarães, CEO da VG Research, ressalta que há mais de 100 empresas
na Bolsa com
dividend yield (taxa de retorno com dividendos) acima de
6% ao ano. Isso mostra que, apesar do rali das últimas semanas de 2023,
ainda há muitas ações descontadas.
Em 2023, os retornos das ações que pagam bons dividendos foram
maiores que dos FIIs. O Índice de Dividendos (IDIV) da B3 subiu 27%,
enquanto o Ifix (índice que acompanha os FIIs mais negociados na Bol-
sa) avançou 15%.
Para 2024, as ações mais citadas por cinco casas de análise consulta-
das pelo InfoMoney como potenciais boas pagadoras de dividendos são
Petrobras, BB Seguridade, Engie e Telefônica Brasil.
No caso da Petrobras (PETR4), embora a companhia tenha perdido o
posto de melhor pagadora de dividendos em 2023 por conta da queda
do faturamento, suas ações
continuam recomendadas.
“A empresa está mudando,
com foco muito mais em in-
vestimentos e menos em di-
videndos. Mas mesmo pa-
gando o mínimo previsto em
sua política, é um valor ele-
vado, pois se trata de uma
forte geradora de caixa”,
afirma Pedro Serra, da Ativa.
Tem muitas ações baratas
ainda, apesar de a bolsa ter
dado o rali no final de ano,
passando de 138 mil pontos.”
Vicente Guimarães, CEO da VG Research
10
ações na bolsa negociam
com
dividend yield
superior a 6% ao ano
100
Mais de
Petrobras
BB Seguridade
Engie
Telefônica Brasil
PETR4
BBSE3
EGIE3
VIVT3
29,22
10,34
7,67
8,16
Empresa Ticker
Dividend yield em 2023 (%)
Ações de dividendos mais recomendadas para 2024
Fonte: Ágora, Ativa, Guide, Terra Investimentos, XP Investimentos e Economática.
Já a BB Seguridade (BBSE3)
foi uma das campeãs de
di-
vidend yield de 2023 (a em-
presa deu retorno com di-
videndos com 10,34%) e a
expectativa dos analistas é
que repita o bom desempenho neste ano. “Os resultados recentes da
companhia demonstram solidez, com um desempenho altamente positi-
vo em todos os segmentos operacionais”, avalia Luis Novaes, analista da
Terra Investimentos. A seguradora vem se expandindo a partir do aumen-
to das parcerias e da penetração nos canais digitais.
A geradora de energia Engie (EGIE3) – historicamente uma boa pagadora
de dividendos – também foi citada pelas casas de análise. Outra ação re-
comendada com frequência é a Telefônica Brasil (VIVT3). A expectativa
é que a distribuição de proventos aumente porque as demandas de in-
vestimentos no setor de telecomunicações está reduzindo em relação ao
passado – com isso, o lucro gerado poderia ser distribuído em maior pro-
porção, em vez de ser reinvestido para o capex.
E quais serão os melhores FIIs para 2024? A queda da Selic deve benefi-
ciar os fundos de shoppings, que podem tanto ter valorização das cotas
quanto aumento dos dividendos, já que as vendas das lojas tendem a au-
mentar. O mesmo se espera dos FIIs de lajes corporativas, um mercado
que pode aquecer, gerando mais dividendos, especialmente nos imóveis
das regiões mais nobres, diz Eduardo Mira, sócio do Clube FII.
Independentemente do momento, o ideal é ter uma carteira equilibrada
(50% e 50%) entre fundos de “tijolo”, que investem diretamente em imó-
veis, e de “papel”, que compram ativos de renda fixa.
Clique e veja as melhores ações de dividendos para 2024
11
BTG Pactual Logística
Hedge Brasil Shopping
VBI Prime Properties
CHSG Logística
Kinea Índices de Preços
BTLG11
HGBS11
PVBI11
HGLG11
KNIP11
8,96
10,33
8,29
9,06
10,68
FundoTicker
Dividend Yield – 12 meses (%)
FIIs mais recomendados para 2024
Fonte: Economática
Em 2023, os fundos de “papel” deram retornos superiores, se compara-
dos aos de “tijolo”. “O motivo para o alto retorno dos FIIs de “papel” se deve
ainda a um período de alta taxa de juros, referência para a rentabilidade
desses fundos”, diz Fernanda Rosalem, head de investimentos da Paladin.
Segundo ela, os fundos de “papel” geralmente são menos voláteis que os
de “tijolo”. Mas, nos fundos de “tijolo”, geralmente o potencial de valoriza-
ção da cota é superior.
Marcos Baroni, head de fundos imobiliários e analista da Suno Research,
espera que os FIIs de “tijolo” sejam os mais beneficiados no ano. Para os
investidores que desejam mais previsibilidade nos retornos, ele recomenda
os fundos com galpões logísticos e shoppings: “Em geral, eles possuem
contratos mais longos e maior estabilidade de fluxo”. Já os fundos de lajes
corporativas podem ser uma alternativa interessante, mas ele diz que o ní-
vel de alavancagem de alguns ainda é elevado, e que eles precisam vender
os imóveis para destravar o valor para os cotistas."""

with conn.cursor() as cur:
    # Define the INSERT query
    insert_query = """
    INSERT INTO vector_table (id, doc_name, text, vector)
    VALUES ('1', 'ebook-onde-investir-2024.pdf', '%s', '%s')
    """  
    print(insert_query)

    # Execute the query
    cur.execute(insert_query)

    # Commit the transaction
    conn.commit()
