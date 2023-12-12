from typing import Dict, cast
from src.Configuration.PresenterConfig import CvePresConfig, PresConf, PresenterId, SavingsPresConfig
from src.Presenter.CsvPresenter import CsvPresenter
from src.Presenter.MultiPresenter import MultiPresenter
from src.Presenter.PresenterException import PresenterException
from src.Presenter.PresenterFactoryException import PresenterFactoryException
from src.Presenter.SavingsPresenter import SavingsPresenter
from src.Presenter.TransactionPresenter import TransactionPresenter


INVALID_INPUT = "no csv output nor pie chart presenter chosen"
PRESENTER_FACTORY_ERROR = "Presenter selection error|what:<{}>"


class PresenterFactory:
    def get(self, c_dict: Dict[PresenterId, PresConf]) -> TransactionPresenter:
        try:
            if self.__multi_pres_enabled(c_dict):
                return self.__create_multi_pres(c_dict)

            if PresenterId.cve in c_dict:
                return self.__create_cve_pres(c_dict[PresenterId.cve])

            elif PresenterId.savings in c_dict:
                return self.__create_savings_pres(c_dict[PresenterId.savings])

        except PresenterException as e:
            msg = PRESENTER_FACTORY_ERROR.format(str(e))
            raise PresenterFactoryException(msg)

        msg = PRESENTER_FACTORY_ERROR.format(INVALID_INPUT)
        raise PresenterFactoryException(msg)

    def __create_cve_pres(self, conf: PresConf) -> CsvPresenter:
        cve_conf: CvePresConfig = cast(CvePresConfig, conf)
        return CsvPresenter(cve_conf)

    def __create_savings_pres(self, conf: PresConf) -> SavingsPresenter:
        save_conf: SavingsPresConfig = cast(SavingsPresConfig, conf)
        return SavingsPresenter(save_conf)

    def __create_multi_pres(self, c_dict: Dict[PresenterId, PresConf]) -> MultiPresenter:
        pres_list = []
        for id, c in c_dict.items():
            pres = self.get({id: c})
            pres_list.append(pres)
        return MultiPresenter(pres_list)

    def __multi_pres_enabled(self, c_dict: Dict[PresenterId, PresConf]) -> bool:
        if len(c_dict) > 1:
            return True
        return False
