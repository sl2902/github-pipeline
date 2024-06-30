

with
    final as (
        select
            repo,
            label,
            num_labels
        from
            {{ ref('int_num_labels_in_issues') }}
)
select
    *
from
    final
order by
    label,
    num_labels desc