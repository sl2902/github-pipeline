

with
    final as (
        select
            repo,
            label,
            num_labels
        from
            {{ ref('fct_num_labels_in_issues') }}
)
select
    *
from
    final
order by
    label,
    num_labels desc