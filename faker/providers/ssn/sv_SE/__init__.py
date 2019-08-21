# coding=utf-8

from __future__ import unicode_literals
from .. import Provider as SsnProvider
import datetime


class Provider(SsnProvider):

    def generate_personnummer(self, min_age, max_age, gender):
        if not gender:
            gender = self.generator.random.choice('FM')
        elif gender not in ('F', 'M'):
            raise ValueError('Gender must be one of F or M.')

        age = datetime.timedelta(
            days=self.generator.random.randrange(min_age * 365, max_age * 365))
        birthday = datetime.datetime.now() - age
        pnr_date = birthday.strftime('%y%m%d')
        if gender == 'F':
            gender_num = self.generator.random.choice((0, 2, 4, 6, 8))
        elif gender == 'M':
            gender_num = self.generator.random.choice((1, 3, 5, 7, 9))
        suffix = str(self.generator.random.randrange(0, 99)).zfill(2) + str(gender_num)
        return pnr_date, suffix

    def generate_organisationsnummer(self, corporate_type):
        if not corporate_type:
            corporate_type = self.generator.random.choice('12356789')
        elif str(corporate_type) not in ['1', '2', '3', '5', '6', '7', '8', '9']:
            raise ValueError('Corporate type must be one digit between 1-3, 5-9.')

        pnr_date = self.bothify('{0}#{1}###'.format(corporate_type, self.generator.random.randrange(2, 10)))
        suffix = self.bothify('###')
        return pnr_date, suffix

    def ssn(self, min_age=18, max_age=90, gender=None, corporate_type=None):
        """
        Returns a 10 digit Swedish SSN, "Personnummer",
        or and Corporate SSN "Organisationsnummer".

        It consists of 10 digits in the form YYMMDD-SSGQ, where
        YYMMDD is the date of birth, SS is a serial number,
        G is the gender identifier (odd for males and even for females)
        and Q is a control character (Luhn checksum).

        http://en.wikipedia.org/wiki/Personal_identity_number_(Sweden)

        It consists of 10 digits in the form AXBXXXX-SSSQ, where
        A is the corporate type, B is a number larger or equal to 2,
        X is random numbers, SSS is a serial number
        and Q is a control character (Luhn checksum).

        https://sv.wikipedia.org/wiki/Organisationsnummer

        :param min_age: minimum age of person
        :type min_age: int
        :param max_age: maximum age of person
        :type min_age: int
        :param gender: gender of the person - "F" for female, M for male.
        :type gender: str
        :param corporate_type: generate a corporate type - 1, 2, 3, 5, 6, 7, 8, 9
        :type corporate_type: int
        :return: Personnummer in str format unless corporate is set then Organisationsnummer
        :rtype: str
        """
        def _luhn_checksum(number):
            def digits_of(n):
                return [int(d) for d in str(n)]
            digits = digits_of(number)
            odd_digits = digits[-1::-2]
            even_digits = digits[-2::-2]
            checksum = 0
            checksum += sum(odd_digits)
            for d in even_digits:
                checksum += sum(digits_of(d * 2))
            return checksum % 10

        def _calculate_luhn(partial_number):
            check_digit = _luhn_checksum(int(partial_number) * 10)
            return check_digit if check_digit == 0 else 10 - check_digit

        if corporate_type:
            pnr_date, suffix = self.generate_organisationsnummer(corporate_type)
        else:
            pnr_date, suffix = self.generate_personnummer(min_age, max_age, gender)

        luhn_checksum = str(_calculate_luhn(pnr_date + suffix))
        pnr = '{0}-{1}{2}'.format(pnr_date, suffix, luhn_checksum)

        return pnr

    vat_id_formats = (
        'SE############',
    )

    def vat_id(self):
        """
        http://ec.europa.eu/taxation_customs/vies/faq.html#item_11
        :return: A random Swedish VAT ID
        """

        return self.bothify(self.random_element(self.vat_id_formats))
