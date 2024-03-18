from asyncio import gather
from fastapi import APIRouter, Path, Query

from converter import sync_converter, async_converter
from schemas import ConverterInput, ConverterOutput


router = APIRouter(prefix='/converter')


@router.get('/{from_currency}/')
def converter(
    *, 
    from_currency: str = Path(max_length=3, regex='^[A-Z]{3}$'),
    to_currencies: str = Query(max_lenght=50, regex='^[A-Z]{3}(,[A-Z]{3})*$'),
    price: float = Query(gt=0)
):
    to_currencies = to_currencies.split(',') #  pyright: ignore

    result = []

    for currency in to_currencies:
        response = sync_converter(
            from_currency=from_currency,
            to_currency=currency,
            price=price
        )
        result.append(response)
    
    return result

@router.get('/async/{from_currency}/')
async def async_converter_router(
    *,
    from_currency: str = Path(max_length=3, regex='^[A-Z]{3}$'),
    to_currencies: str = Query(max_lenght=50, regex='^[A-Z]{3}(,[A-Z]{3})*$'),
    price: float = Query(gt=0)
):
    to_currencies = to_currencies.split(',')  # pyright: ignore

    courotines = []

    for currency in to_currencies:
        coro = async_converter(
            from_currency=from_currency,
            to_currency=currency,
            price=price
        )
        courotines.append(coro)
    
    result = await gather(*courotines)
    
    return result

@router.post('/async/v2/{from_currency}/', response_model=ConverterOutput)
async def async_converter_router_v2(
    *,
    converter: ConverterInput,
    from_currency: str = Path(max_length=3, regex='^[A-Z]{3}(,[A-Z]{3})*$')
):
    to_currencies = converter.to_currencies
    price = converter.price

    couroutines = []

    for currency in to_currencies:
        coro = async_converter(
            from_currency=from_currency,
            to_currency=currency,
            price=price
        )

        couroutines.append(coro)
    
    result = await gather(*couroutines)
    
    return ConverterOutput(
        message='success',
        data=result
    )

