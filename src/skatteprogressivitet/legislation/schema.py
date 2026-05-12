"""Pydantic v2 models for the legislative-parameter ledger.

Each model corresponds to a section of the per-year YAML files validated by
``data/legislation/schema.json``. Field validators enforce monotone bracket
thresholds and non-negative rates.
"""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field, model_validator


class Bracket(BaseModel):
    """A single marginal-rate bracket.

    Attributes:
        lower: Lower bound of the bracket (inclusive), in SEK.
        upper: Upper bound (exclusive), or ``None`` for the top bracket.
        rate: Marginal rate applied within the bracket.
    """

    lower: float = Field(ge=0)
    upper: Optional[float] = None
    rate: float = Field(ge=0, le=1)

    model_config = {"frozen": True}


class StatligSkatt(BaseModel):
    """State income tax bracket schedule.

    Attributes:
        brackets: Ordered list of :class:`Bracket` objects.
        notes: Optional annotation.
    """

    brackets: list[Bracket]
    notes: str = ""

    model_config = {"frozen": True}

    @model_validator(mode="after")
    def _monotone_brackets(self) -> "StatligSkatt":
        """Validate that bracket lower bounds are strictly increasing.

        Returns:
            Self after validation.

        Raises:
            ValueError: If any bracket's lower bound is not greater than the prior.
        """
        lowers = [b.lower for b in self.brackets]
        for i in range(1, len(lowers)):
            if lowers[i] <= lowers[i - 1]:
                raise ValueError(
                    f"Bracket lower bounds must be strictly increasing; "
                    f"got {lowers[i]} after {lowers[i - 1]}."
                )
        return self


class KommunalSkatt(BaseModel):
    """Municipal income tax parameters.

    Attributes:
        rate: Proportional municipal rate (national average).
        notes: Optional annotation.
    """

    rate: float = Field(ge=0, le=1)
    notes: str = ""

    model_config = {"frozen": True}


class Kapitalinkomstskatt(BaseModel):
    """Capital-income tax parameters.

    Attributes:
        standard_rate: Standard flat rate on net capital income.
        dividend_rate: Optional specific dividend rate.
        notes: Optional annotation.
    """

    standard_rate: float = Field(ge=0, le=1)
    dividend_rate: Optional[float] = Field(default=None, ge=0, le=1)
    notes: str = ""

    model_config = {"frozen": True}


class Arbetsgivaravgift(BaseModel):
    """Employer payroll tax parameters.

    Attributes:
        rate: Standard employer social contribution rate.
        ceiling: Optional income ceiling; ``None`` = no ceiling.
        reduced_rate_under_26: Reduced rate for workers under 26.
        reduced_rate_over_65: Reduced rate for workers over 65.
        notes: Optional annotation.
    """

    rate: float = Field(ge=0, le=1)
    ceiling: Optional[float] = None
    reduced_rate_under_26: Optional[float] = Field(default=None, ge=0, le=1)
    reduced_rate_over_65: Optional[float] = Field(default=None, ge=0, le=1)
    notes: str = ""

    model_config = {"frozen": True}


class Egenavgift(BaseModel):
    """Self-employed social contribution parameters.

    Attributes:
        rate: Self-employed contribution rate.
        ceiling: Optional income ceiling; ``None`` = no ceiling.
        notes: Optional annotation.
    """

    rate: float = Field(ge=0, le=1)
    ceiling: Optional[float] = None
    notes: str = ""

    model_config = {"frozen": True}


class JSSSegment(BaseModel):
    """One segment of the jobbskatteavdrag piecewise schedule.

    Attributes:
        income_lower: Lower income bound for this segment, in SEK.
        income_upper: Upper income bound, or ``None`` for the top segment.
        formula: String formula (informational; not eval'd at runtime).
        max_credit: Optional maximum credit cap for this segment.
    """

    income_lower: float = Field(ge=0)
    income_upper: Optional[float] = None
    formula: str
    max_credit: Optional[float] = None

    model_config = {"frozen": True}


class Jobbskatteavdrag(BaseModel):
    """Earned-income tax credit (jobbskatteavdrag) parameters.

    Attributes:
        enabled: Whether the credit is active for this year.
        schedule: Piecewise schedule segments.
        age_65_plus_enhanced: Whether the enhanced over-65 credit applies.
        notes: Optional annotation.
    """

    enabled: bool
    schedule: list[JSSSegment] = Field(default_factory=list)
    age_65_plus_enhanced: bool = False
    notes: str = ""

    model_config = {"frozen": True}


class ThreeTwelve(BaseModel):
    """3:12 rules for closely held firms (fåmansföretag).

    Attributes:
        enabled: Whether the 3:12 rules apply this year.
        forenklingsregeln_base: Base amount for förenklingsregeln, in SEK.
        forenklingsregeln_rate: Rate applied to base (usually 0; base is the cap).
        huvudregeln_return_rate: Required return rate for huvudregeln.
        dividend_rate_qualified: Tax rate on qualified dividends.
        dividend_rate_excess: Effective rate on excess dividends (labour income).
        notes: Optional annotation.
    """

    enabled: bool = True
    forenklingsregeln_base: float = Field(ge=0)
    forenklingsregeln_rate: float = Field(ge=0, le=1)
    huvudregeln_return_rate: float = Field(ge=0, le=1)
    dividend_rate_qualified: float = Field(ge=0, le=1)
    dividend_rate_excess: float = Field(ge=0, le=1)
    notes: str = ""

    model_config = {"frozen": True}


class HousingAllowance(BaseModel):
    """Housing allowance parameters.

    Attributes:
        bostadsbidrag_max: Maximum annual bostadsbidrag, in SEK.
        bostadstillagg_max: Maximum annual bostadstillagg, in SEK.
        income_taper_rate: Rate at which allowances taper with income.
        notes: Optional annotation.
    """

    bostadsbidrag_max: float = Field(ge=0)
    bostadstillagg_max: float = Field(ge=0)
    income_taper_rate: float = Field(ge=0, le=1)
    notes: str = ""

    model_config = {"frozen": True}


class Transfers(BaseModel):
    """Social transfer replacement-rate parameters.

    Attributes:
        sjukpenning_rate: Sickness benefit replacement rate.
        foraldrapenning_rate: Parental benefit replacement rate.
        a_kassa_rate: Unemployment benefit replacement rate.
        a_kassa_ceiling_ibb_fraction: A-kassa ceiling as fraction of IBB.
        notes: Optional annotation.
    """

    sjukpenning_rate: float = Field(ge=0, le=1)
    foraldrapenning_rate: float = Field(ge=0, le=1)
    a_kassa_rate: float = Field(ge=0, le=1)
    a_kassa_ceiling_ibb_fraction: float = Field(ge=0)
    notes: str = ""

    model_config = {"frozen": True}


class Legislation(BaseModel):
    """Complete legislative parameters for a single reform year.

    Attributes:
        year: The reform year.
        sfs_reference: SFS reference string.
        prop_reference: Government proposition reference.
        effective_date: Date the parameters took effect.
        notes: Optional annotation.
        kommunal_skatt: Municipal income tax parameters.
        statlig_skatt: State income tax bracket schedule.
        kapitalinkomstskatt: Capital-income tax parameters.
        arbetsgivaravgift: Employer payroll tax parameters.
        egenavgift: Self-employed social contribution parameters.
        jobbskatteavdrag: Earned-income tax credit parameters.
        three_twelve: 3:12 rules parameters.
        housing_allowance: Housing allowance parameters.
        transfers: Social transfer parameters.
        basbelopp: Basbelopp for this year, in SEK.
        prisbasbelopp: Prisbasbelopp for this year, in SEK.
        inkomstbasbelopp: Inkomstbasbelopp for this year, in SEK.
    """

    year: int = Field(ge=1991, le=2100)
    sfs_reference: str = ""
    prop_reference: str = ""
    effective_date: str = ""
    notes: str = ""

    kommunal_skatt: KommunalSkatt
    statlig_skatt: StatligSkatt
    kapitalinkomstskatt: Kapitalinkomstskatt
    arbetsgivaravgift: Arbetsgivaravgift
    egenavgift: Egenavgift
    jobbskatteavdrag: Jobbskatteavdrag
    three_twelve: Optional[ThreeTwelve] = None
    housing_allowance: Optional[HousingAllowance] = None
    transfers: Optional[Transfers] = None

    basbelopp: float = Field(ge=0)
    prisbasbelopp: float = Field(ge=0)
    inkomstbasbelopp: float = Field(ge=0)

    model_config = {"frozen": True}
