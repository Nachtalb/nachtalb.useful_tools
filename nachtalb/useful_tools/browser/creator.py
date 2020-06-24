from plone import api
from plone.app.textfield.value import RichTextValue
from zope.interface import implements

from nachtalb.useful_tools.browser.useful_tools import UsefulToolsView
from nachtalb.useful_tools.interfaces import ICreatorInterface


class CreatorView(UsefulToolsView):
    implements(ICreatorInterface)

    default = [{
        'type': 'ftw.simplelayout.ContentPage',
        'title': 'ContentPasche',
        'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Hosne igitur laudas et hanc eorum, inquam, sententiam sequi nos censes oportere? Suam denique cuique naturam esse ad vivendum ducem. Vide igitur ne non debeas verbis nostris uti, sententiis tuis. Duo Reges: constructio interrete. Idem etiam dolorem saepe perpetiuntur, ne, si id non faciant, incidant in maiorem. Si longus, levis;',
        'children': [{
            'type': 'ftw.simplelayout.TextBlock',
            'title': 'TextBlock 1',
            'text': RichTextValue(
                raw=('<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Respondent extrema primis, media utrisque, omnia omnibus. Quae cum dixisset paulumque institisset, Quid est? An vero, inquit, quisquam potest probare, quod perceptfum, quod. Si verbum sequimur, primum longius verbum praepositum quam bonum. Ergo in gubernando nihil, in officio plurimum interest, quo in genere peccetur. Duo Reges: constructio interrete. Sed fortuna fortis; Quo tandem modo? Hoc ille tuus non vult omnibusque ex rebus voluptatem quasi mercedem exigit. Sin laboramus, quis est, qui alienae modum statuat industriae? </p>'
                     '<p>Unum nescio, quo modo possit, si luxuriosus sit, finitas cupiditates habere. Omnia contraria, quos etiam insanos esse vultis. Atque haec coniunctio confusioque virtutum tamen a philosophis ratione quadam distinguitur. Est igitur officium eius generis, quod nec in bonis ponatur nec in contrariis. Mihi quidem Antiochum, quem audis, satis belle videris attendere. Tenesne igitur, inquam, Hieronymus Rhodius quid dicat esse summum bonum, quo putet omnia referri oportere? Cur, nisi quod turpis oratio est? Etenim semper illud extra est, quod arte comprehenditur. In qua si nihil est praeter rationem, sit in una virtute finis bonorum; Quod autem in homine praestantissimum atque optimum est, id deseruit.</p>'
                     '<p>Negat enim summo bono afferre incrementum diem. Bonum integritas corporis: misera debilitas. Longum est enim ad omnia respondere, quae a te dicta sunt. Si autem id non concedatur, non continuo vita beata tollitur. An est aliquid per se ipsum flagitiosum, etiamsi nulla comitetur infamia? Et quidem, inquit, vehementer errat; Nec vero alia sunt quaerenda contra Carneadeam illam sententiam.</p>'),
            )
        }],
    }]

    def create(self, object_infos, container):
        for obj_info in object_infos:
            children = []

            if 'children' in obj_info:
                children = obj_info.pop('children')

            new_obj = api.content.create(container=container, **obj_info)
            yield new_obj

            for child in children:
                for new_child in self.create(children, new_obj):
                    yield new_child

    def sl(self):
        """Create simplelayout content"""
        logger = self.get_logger(with_timestamp=False)
        context = self.get_non_ut_context()
        for new_obj in self.create(self.default, context):
            logger.info('New object <a href="{}" target="_blank">"{}" ({})</a>'.format(
                new_obj.absolute_url(),
                new_obj.title,
                new_obj.id,
            ))
        logger.info('Done')

    def other(self):
        """Generic creator"""
        logger = self.get_logger(with_timestamp=False)
        logger.info('Not yet implemented')

